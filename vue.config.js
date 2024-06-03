const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  // transpileDependencies: true,
  pluginOptions: {
    electronBuilder: {
      builderOptions: {
        // options placed here will be merged with default configuration and passed to electron-builder
        productName: "Covid Outcome Probability Prediction",
        win: {
          icon: './src/assets/virus.png'
        },
        nsis: {

        },
        files: [
          "**/*"
        ],
        extraFiles: [
          {
              "from": "script/build",
              "to": "script/build",
              "filter": ["**/*"]
          },
          {
              "from": "script/dist",
              "to": "script/dist",
              "filter": ["**/*"]
          }
        ]
      }
    }
  }
})
