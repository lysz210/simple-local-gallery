import { defineConfig } from "@hey-api/openapi-ts"

export default defineConfig({
  input: "http://localhost:8000/api/v1/openapi.json",
  output: "./src/slg-api",
  plugins: [
    '@hey-api/typescript',
    '@hey-api/client-axios',
    {
      name: "@hey-api/sdk",
      // NOTE: this doesn't allow tree-shaking
      asClass: true,
      operationId: false
    }
  ]
})
