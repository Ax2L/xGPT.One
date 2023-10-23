## Run.sh:
The script manages a deployment flow for a given application. Here's what it does step by step:

1. **Repository Management**: 
    - If the repository already exists in the temp directory, it updates the repository from GitHub.
    - If not, it clones the repository from GitHub.

2. **Configuration Management**:
    - Copies the `config.yaml` from the application path to the cloned repository's path.
    - Copies all files within the `docker` directory of the application path to the cloned repository's path.
    - Verifies the SSL certificate for its validity. If the certificate isn't valid, it runs a script (`certificate.sh`) to handle it.

3. **Nginx Configuration**:
    - Checks if there are any changes between the `nginx.conf` of the application and the system's `nginx.conf`.
    - If there's a change, it stops the nginx service, copies the new configuration, and then restarts the nginx service.

4. **Docker Management**:
    - It brings up the application using Docker (ensuring all defined services are running in the background) and then displays the logs.

To use the script, make sure you have:
- A proper `x.conf` file with the necessary details.
- Proper permissions to execute the script and access to the paths mentioned in `x.conf`.
- Installed tools like `git`, `openssl`, `systemctl`, and `docker-compose`.

Save the script as `deploy.sh` or any name you prefer. Provide execute permissions using `chmod +x deploy.sh` and run the script using `./deploy.sh`.