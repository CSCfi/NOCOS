## DESP Account and aquiering the rights to data
See [https://platform.destine.eu/](https://platform.destine.eu/)

## DESP and CacheB Authentication Scripts

To access protected Climate DT data and services (such as Polytope API and the CacheB data cache), authentication using your DESP (Destination Earth Service Platform) credentials is required.  
Two provided scripts automate the login process and retrieval of refresh tokens needed for secure access.

### Functionality

- Prompt for your DESP username and password (or use command line arguments or environment variables).
- Authenticate against the DESP IAM server.
- Retrieve a refresh token required for further data/API requests.
- Output the token either to a file (for use by other tools) or in a configuration block for use in client applications.

These scripts enable:

- **Access to the Polytope API** for advanced data and service requests.
- **Access to the CacheB data cache** for efficient data retrieval workflows.

### Usage

- [`desp-authentication.py`](lib/desp-authentication.py):  
  Retrieves a refresh token for the Polytope API, and stores it (default: `~/.polytopeapirc`) or prints to stdout.

- [`cacheb-authentication.py`](lib/cacheb-authentication.py):  
  Retrieves a refresh token and prints out a configuration block suitable for accessing the CacheB data cache service.

**Refer to each script for details, command-line options, and example usage.**

---

> **Note:**  
> The most up-to-date authentication scripts and templates can be found on the DESP platform (INSULA) or in the dedicated DESP code repositories, which are included as submodules in this project:
>
> - [`lib/polytope-examples`](lib/polytope-examples)  
>   [https://github.com/destination-earth-digital-twins/polytope-examples](https://github.com/destination-earth-digital-twins/polytope-examples)
>
> - [`lib/DESP-UserWorkflowService-Templates`](lib/DESP-UserWorkflowService-Templates)  
>   [https://github.com/SercoSPA/DESP-UserWorkflowService-Templates](https://github.com/SercoSPA/DESP-UserWorkflowService-Templates)

### How to Use

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

2. **Run the desired script:**  
    For Polytope API authentication:
    ```sh
    python path/to/desp-authentication.py
    ```
    For CacheB authentication:
    ```sh
    python path/to/cacheb-authentication.py
    ```

3. **Provide credentials:**
    - The script will prompt you for your DESP username and password unless provided as command line arguments or environment variables.

4. **Result:**
    - For Polytope API:  
      By default, your refresh token is saved to `~/.polytopeapirc` (in your home directory).  
      You can change the output file with `-o <filename>` or print directly to the terminal using `-o stdout`.
    - For CacheB:  
      The script prints out a configuration block with your refresh token for use with the `cacheb.dcms.destine.eu` service.

### Command-line options

- `-u, --user` — DESP username (can also use `USER` env variable)
- `-p, --password` — DESP password (can also use `PASSWORD` env variable)
- `-o, --outpath` — Output file for the token (default: `~/.polytopeapirc`, or use `"stdout"`)  
  *(Polytope API script only)*

**Example usage:**
```sh
python desp-authentication.py -u 'myusername' -p 'mypassword' -o mytoken.json
python cacheb-authentication.py -u 'myusername' -p 'mypassword'

Back to [common README.md](README.md)

[NOCOS github front page](../README.md).