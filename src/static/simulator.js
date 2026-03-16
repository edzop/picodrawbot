// Browser-side simulator for picodrawbot commands
// Mirrors the Python command_processor.py and command_handler.py logic

class CommandProcessor {
    constructor() {
        this.commandList = [];
    }

    getCommands() {
        return this.commandList;
    }

    tokenize(data) {
        const tokens = [];
        for (const line of data.split('\n')) {
            const stripped = line.split('#')[0];
            tokens.push(...stripped.trim().split(/\s+/).filter(s => s.length > 0));
        }
        return tokens;
    }

    parseBlock(tokens, index) {
        const commands = [];
        while (index < tokens.length) {
            const token = tokens[index];

            if (token === ']') {
                return [commands, index + 1];
            }

            if (token.toUpperCase() === 'REPEAT') {
                const count = parseInt(tokens[index + 1], 10);
                index += 2;
                if (index < tokens.length && tokens[index] === '[') {
                    index += 1; // skip [
                }
                let blockCommands;
                [blockCommands, index] = this.parseBlock(tokens, index);
                for (let i = 0; i < count; i++) {
                    commands.push(...blockCommands);
                }

            } else if (token.toUpperCase() === 'FOR') {
                const start = parseInt(tokens[index + 1], 10);
                const end = parseInt(tokens[index + 2], 10);
                index += 3;
                let step;
                if (index < tokens.length && tokens[index] !== '[' && tokens[index] !== ']' && /^-?\d+$/.test(tokens[index])) {
                    step = parseInt(tokens[index], 10);
                    index += 1;
                } else {
                    step = 1;
                }
                if (index < tokens.length && tokens[index] === '[') {
                    index += 1; // skip [
                }
                let blockCommands;
                [blockCommands, index] = this.parseBlock(tokens, index);
                for (let i = start; i <= end; i += step) {
                    for (const cmd of blockCommands) {
                        commands.push([cmd[0], cmd[1] === '$i' ? i : cmd[1]]);
                    }
                }

            } else if (index + 1 < tokens.length && (/^\d+$/.test(tokens[index + 1]) || tokens[index + 1] === '$i')) {
                const raw = tokens[index + 1];
                commands.push([token.toUpperCase(), raw === '$i' ? raw : parseInt(raw, 10)]);
                index += 2;

            } else {
                index += 1;
            }
        }
        return [commands, index];
    }

    processRawInput(data) {
        this.commandList = [];
        const tokens = this.tokenize(data);
        [this.commandList] = this.parseBlock(tokens, 0);
    }
}

class RobotSimulator {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.reset();
    }

    reset() {
        this.x = this.canvas.width / 2;
        this.y = this.canvas.height / 2;
        this.angle = -Math.PI / 2; // facing up
        this.path = [{ x: this.x, y: this.y }];
        this.speed = 20;
        this.direction = 1;
        this.STEP_PX = 3; // pixels per step
        this.TURN_DEG = 3; // degrees per step for LT/RT
    }

    handleCommand(command) {
        const name = command[0];
        const parm = command[1];
        const steps = parm * this.direction;

        if (name === 'LT') {
            this.angle -= (steps * this.TURN_DEG * Math.PI) / 180;
            return `stepL: ${steps}`;
        }
        if (name === 'RT') {
            this.angle += (steps * this.TURN_DEG * Math.PI) / 180;
            return `stepR: ${steps}`;
        }
        if (name === 'ST' || name === 'FW') {
            this.x += Math.cos(this.angle) * steps * this.STEP_PX;
            this.y += Math.sin(this.angle) * steps * this.STEP_PX;
            this.path.push({ x: this.x, y: this.y });
            return `stepS: ${steps}`;
        }
        if (name === 'BW') {
            this.x -= Math.cos(this.angle) * steps * this.STEP_PX;
            this.y -= Math.sin(this.angle) * steps * this.STEP_PX;
            this.path.push({ x: this.x, y: this.y });
            return `stepBW: ${steps}`;
        }
        if (name === 'SP') {
            this.speed = parm;
            return `speed: ${parm}`;
        }
        if (name === 'DR') {
            this.direction = parm === 0 ? -1 : 1;
            return `direction: ${this.direction}`;
        }
        if (name === 'DL') {
            return `delay: ${parm / 10}`;
        }
        if (name === 'BL') {
            return `blink(${parm})`;
        }
        return '-';
    }

    draw() {
        const ctx = this.ctx;
        const w = this.canvas.width;
        const h = this.canvas.height;

        ctx.clearRect(0, 0, w, h);

        // Grid
        ctx.strokeStyle = '#e8e8e8';
        ctx.lineWidth = 1;
        for (let gx = 0; gx < w; gx += 20) {
            ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, h); ctx.stroke();
        }
        for (let gy = 0; gy < h; gy += 20) {
            ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(w, gy); ctx.stroke();
        }

        // Center crosshair
        ctx.strokeStyle = '#ccc';
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(w / 2, 0); ctx.lineTo(w / 2, h); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, h / 2); ctx.lineTo(w, h / 2); ctx.stroke();

        if (this.path.length < 1) return;

        // Draw path
        ctx.strokeStyle = '#2196F3';
        ctx.lineWidth = 2;
        ctx.lineJoin = 'round';
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(this.path[0].x, this.path[0].y);
        for (let i = 1; i < this.path.length; i++) {
            ctx.lineTo(this.path[i].x, this.path[i].y);
        }
        ctx.stroke();

        // Start dot
        ctx.fillStyle = '#4CAF50';
        ctx.beginPath();
        ctx.arc(this.path[0].x, this.path[0].y, 5, 0, Math.PI * 2);
        ctx.fill();

        // Robot position
        ctx.fillStyle = '#F44336';
        ctx.beginPath();
        ctx.arc(this.x, this.y, 6, 0, Math.PI * 2);
        ctx.fill();

        // Direction arrow
        const arrowLen = 14;
        ctx.strokeStyle = '#F44336';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(
            this.x + Math.cos(this.angle) * arrowLen,
            this.y + Math.sin(this.angle) * arrowLen
        );
        ctx.stroke();
    }

    run(rawInput) {
        this.reset();
        const processor = new CommandProcessor();
        processor.processRawInput(rawInput);
        const results = [];
        for (const cmd of processor.getCommands()) {
            const r = this.handleCommand(cmd);
            results.push(`${r}(${cmd[0]} ${cmd[1]})`);
        }
        this.draw();
        return results;
    }
}

// Initialize simulator when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('sim_canvas');
    if (!canvas) return;

    const sim = new RobotSimulator(canvas);
    sim.draw();

    const simButton = document.getElementById('sim_button');

    if (simButton) {
        simButton.addEventListener('click', ev => {
            ev.preventDefault();
            const text = document.getElementById('command').value;
            const results = sim.run(text);
            const lines = results.length ? results : ['(no commands)'];
            lines.forEach(r => log(r, 'green'));
        });
    }

    const resetButton = document.getElementById('sim_reset');
    if (resetButton) {
        resetButton.addEventListener('click', ev => {
            ev.preventDefault();
            sim.reset();
            sim.draw();
            if (simLog) simLog.innerHTML = '';
        });
    }
});
