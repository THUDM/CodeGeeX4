# Local Mode Tutorial: Local deployment with the Visual Studio Code / Jetbrains extensions

The steps for two platforms are the same.
1. Click [VS Code](https://marketplace.visualstudio.com/items?itemName=aminer.codegeex) / [Jetbrains](https://plugins.jetbrains.com/plugin/20587-codegeex) to download the extension.
2. Open the local mode in the extension settings (no need to login).
3. Start Ollama server (other OpenAI compatible APIs are also supported) with the following command (keep the server running in background):

    ```bash
    export OLLAMA_ORIGINS="*"
    ollama run codegeex4
    ollama serve
    ```
4. Enter the api address and model name in local mode settings. Then enjoy coding with CodeGeeX4!

    ![local mode](../resources/local_mode.png)

