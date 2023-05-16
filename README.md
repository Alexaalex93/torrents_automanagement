# Torrent Auto Management Script

This script automatically manages downloaded movies and series. It renames and moves files, scrapes information from online databases, uploads the files to Google Drive, and logs activities.

## Features

- File renaming and moving
- Information scraping
- File upload to Google Drive
- Logging of activities

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Alexaalex93/torrents_automanagement.git
    ```

2. Navigate to the project directory:

    ```bash
    cd torrents_automanagement
    ```

3. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

5. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with the required arguments:

```bash
python main.py --source_path [Path of the download] --category [Torrent category] --tracker [Torrent tracker]
```
Replace the bracketed sections with your specific information.

## Configuration

## Docker Torrent Client Configuration

In order to successfully use the `tinyMediaManager` Docker container in your setup, you must specify the correct download mount point for your torrent client Docker container in the `app_configuration.json` file.

This mount point is the location in the host system where the torrent client's downloaded files are stored. It's typically set when the torrent client container is created, and it allows other containers and applications to access the downloaded files.

Two configuration files are required to run this application: `bot_configuration.json` and `app_configuration.json`.

### app_configuration.json

This file contains the application configuration. Here's an example:

```json

{
    "rclone_path":"/path/to/rclone",
    "rclone_config_path":"",
    "tmm_configuration_path":"/path/to/data",
	"downloads_mount_point": "/path/to/your/download/folder"
}
```

Replace the values with your actual configuration.

### bot_configuration.json

This file contains the configuration for the Telegram bot. Here's an example:

```json
{
    "chat_id_logs":"xxxxxxxxxxxxx",
    "chat_id_channel":"xxxxxxxxxxxxx",
    "bot_token_channel":"xxxxxxxx:XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "bot_token_logs":"xxxxxxxxxxxx1:XXXXXXXXXXXXXXXXXXXXXXXXX"
}
```
Replace the values with your actual Telegram bot configuration.

Remember to rename the sample configuration files to `bot_configuration.json` and `app_configuration.json` and place them in the config/ directory.

## Docker Image Configuration

This project utilizes the Docker image `alexaalex93/tinymediamanager_cli_ubuntu`, which includes the tinyMediaManager software. 

To function correctly, you will need to provide the necessary configuration for tinyMediaManager. If no configuration is provided, the script will fail. The configuration can be the default one, but it's crucial to specify the correct path to it.

To get this configuration, you can download and run tinyMediaManager on any platform. Upon launching, a `data` folder will be created within the tinyMediaManager directory, containing the necessary configuration files.

You need to provide a path to this `data` folder, which includes all the configuration for movies, TV shows, tinyMediaManager settings, and even a license if one has been purchased.

To modify the configuration, you can either directly edit `movies.json`, `tvShows.json`, and `tmm.json` files, or launch tinyMediaManager on your platform, make the necessary changes, and then copy the `data` folder to a directory of your choice. The path to this directory should then be specified in the bot's configuration or directly provided as the path to the `data` folder.

## Rclone Configuration

This script uses [Rclone](https://rclone.org/) to upload files to Google Drive. You must set up Rclone and configure it with the name of the remote that matches the category you have added in the torrent client, as this name will be used as the remote to upload to.

## Logging Configuration and Customization

To configure and customize the logs, you can modify the files in the `templates/` directory. If you need to create additional template files, remember to update the code to use the new templates.

## .gitignore

This project uses a `.gitignore` file to prevent certain files and directories from being uploaded to the repository. The following are not uploaded:

- `config/`: This directory contains configuration files which may contain sensitive data. A sample configuration file is provided as `config_sample/`.
- `__pycache__/`: This directory is generated by Python and contains byte code files. It is not necessary to include it in the repository.
- `logs/`: This directory contains log files generated by the application.

To add or remove files or directories from `.gitignore`, modify the `.gitignore` file in the root directory of the project.

## Tests

Tests are included in the `tests/` directory. While these are not uploaded to the repository by default (due to the `.gitignore` file), you may choose to include them if you wish.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Author

This project was created by [Alex](mailto:alex.fernandez.0393@gmail.com). You may contact the author for further information or assistance.
