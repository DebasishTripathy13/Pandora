import type { Command } from "./types.js";

const quit: Command = {
  name: "quit",
  description: "Exit Pandora CLI",
  aliases: ["exit"],
  execute(_args, ctx) {
    ctx.exit();
  },
};

export default quit;
