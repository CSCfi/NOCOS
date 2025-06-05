## DESP Account and aquiering the rights to data
See [https://platform.destine.eu/](https://platform.destine.eu/)

## DESP Authentication Script

This script authenticates a user with the **DESP (Destination Earth Service Platform)** and retrieves a refresh token, which is needed to access protected Climate DT data and APIs.

### What does it do?

- Prompts for your DESP username and password (or reads them from command line arguments or environment variables).
- Authenticates against the DESP Identity and Access Management (IAM) server.
- Obtains a refresh token for the [Polytope API](https://polytope.lumi.apps.dte.destination-earth.eu/).
- Stores the token in a file (`~/.polytopeapirc` by default) or prints it to `stdout` if requested.

### How to use

1. **Install dependencies:**

    You’ll need Python and the following libraries:
    - `requests`
    - `conflator`
    - `lxml`
    - `pydantic`

    Install them with pip if needed:
    ```sh
    pip install requests conflator lxml pydantic
    ```

2. **Run the script:**
    ```sh
    python path/to/desp-authentication.py
    ```

3. **Provide credentials:**
    - The script will prompt you for your DESP username and password unless provided as command line arguments or environment variables.

4. **Result:**
    - By default, your refresh token is saved to `~/.polytopeapirc` (in your home directory).
    - You can change the output file with `-o <filename>` or print directly to the terminal using `-o stdout`.

### Command-line options

- `-u, --user` — DESP username (can also use `USER` env variable)
- `-p, --password` — DESP password (can also use `PASSWORD` env variable)
- `-o, --outpath` — Output file for the token (default: `~/.polytopeapirc`, or use `"stdout"`)

**Example:**
```sh
python despauth.py -u myusername -p mypassword -o mytoken.json
```

Back to [common README.md](README.md)

[NOCOS github front page](../README.md).