import { fileURLToPath } from "node:url";

const newE2E = process.env.TEST_MODE === "e2e";
const newE2ETests = "./src/__tests__/e2e/**/*.spec.ts";

const fromServerRoot = (relativePath) =>
  fileURLToPath(new URL(relativePath, import.meta.url));

const preludes = [fromServerRoot("./src/prelude.ts")];

if (newE2E) {
  preludes.push(fromServerRoot("./src/__tests__/e2e/prelude.ts"));
}

export default {
  timeout: "1m",
  nodeArguments: ["--import=tsx"],
  extensions: {
    ts: "module",
  },
  watchMode: {
    ignoreChanges: ["**/*.gen.*"],
  },
  files: newE2E
    ? [newE2ETests]
    : ["**/*.spec.ts", "**/*.e2e.ts", "!" + newE2ETests],
  require: preludes,
  environmentVariables: {
    NODE_ENV: "test",
    DEPLOYMENT_TYPE: "sisonotes",
    MAILER_HOST: "0.0.0.0",
    MAILER_PORT: "1025",
    MAILER_USER: "noreply@siso.agency",
    MAILER_PASSWORD: "sisonotes",
    MAILER_SENDER: "noreply@siso.agency",
  },
};
