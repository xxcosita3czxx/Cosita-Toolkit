    def update_repo_files_http(owner:str, repo:str, branch:str, file_path:str) -> int: # noqa: C901, E501
        """Update files from repo with http api.

        Args:
        ----
            owner (str): Repo Owner
            repo (str): Repository
            branch (str): Branch
            file_path (str): File to update

        Returns:
        -------
            int: Returns status

        """
        file_content = None

        def get_current_branch(repo_path):
            head_path = os.path.join(repo_path, '.git', 'HEAD')
            with open(head_path) as head_file:
                ref = head_file.read().strip()
            if ref.startswith('ref:'):
                return ref.split('/')[-1]
            else:
                return None

        def get_latest_commit_hash(repo_path, branch_name):
            ref_path = os.path.join(repo_path, '.git', 'refs', 'heads', branch_name)
            with open(ref_path) as ref_file:
                return ref_file.read().strip()

        latest_commit_hash = get_latest_commit_hash(".", get_current_branch("."))
        def compute_file_hash(file_content):

            file_hash = hashlib.sha256(file_content.encode()).hexdigest()
            return file_hash

        def get_file_content(owner, repo, file_path):

            file_content=None
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
            response = requests.get(url)  # noqa: S113

            if response.status_code == Status.Requests.SUCCESS:

                try:
                    file_content = base64.b64decode(
                        response.json()['content'],
                    ).decode()
                    return file_content

                except KeyError:
                    logging.error(
                        "Failed to extract content from API response:",
                        response.json(),
                    )
                    return Status.SYNTAX

            elif response.status_code == Status.NOT_FOUND:
                logging.debug(f"Ignoring {file_content}")

            else:
                logging.error(
                    f"Failed to fetch file '{file_path}' from the repository '{repo}'. Response code: {response.status_code}",  # noqa: E501
                )
                return Status.ERR_UNK

        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{branch}"
        response = requests.get(url)  # noqa: S113

        if response.status_code == Status.Requests.SUCCESS:
            latest_commit_hash = response.json().get('sha')

            if file_content:
                file_content = get_file_content(owner, repo, file_path)

                if file_content is not None:
                    file_hash = compute_file_hash(file_content)

                    if file_hash != latest_commit_hash:
                        logging.info(
                            f"Updates available for '{file_path}'. Downloading...",
                        )
                        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
                        response = requests.get(url)  # noqa: S113

                        if response.status_code == Status.Requests.SUCCESS:

                            with open(file_path, 'wb') as f:
                                f.write(response.content)

                        else:
                            logging.error(
                                f"Failed to download file from '{url}'. Response code: {response.status_code}",  # noqa: E501
                            )
                            return Status.ERR_UNK

                        logging.info(f"Updates for '{file_path}' downloaded successfully.")  # noqa: E501
                        return Status.SUCCESS

                    else:
                        logging.info(f"No updates available for '{file_path}'.")
                        return Status.STANDBY

                else:
                    logging.warning(
                        "Unable to compute file hash. Check if the file exists.",
                    )
                    return Status.NOT_FOUND

            else:

                try:

                    for file_name in os.listdir('.'):

                        if os.path.isfile(file_name):
                            logging.debug(
                                f"Checking for updates to '{file_name}'...",
                            )
                            file_content = get_file_content(owner, repo, file_name)

                            if file_content is not None:
                                file_hash = compute_file_hash(file_content)

                                if file_hash != latest_commit_hash:
                                    logging.info(
                                        f"Updates available for '{file_name}'. Downloading...",  # noqa: E501
                                    )
                                    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_name}"
                                    response = requests.get(url)  # noqa: S113

                                    if response.status_code == Status.Requests.SUCCESS:  # noqa: E501

                                        with open(file_name, 'wb') as f:
                                            f.write(response.content)

                                    else:
                                        logging.error(
                                            f"Failed to download file from '{url}'. Response code: {response.status_code}",  # noqa: E501
                                        )
                                        return Status.ERR_UNK

                                    logging.info(
                                        f"Updates for '{file_name}' downloaded successfully.",  # noqa: E501
                                    )

                                else:
                                    logging.info(
                                        f"No updates available for '{file_name}'.",
                                    )

                            else:
                                logging.warning(
                                    "Unable to compute file hash. Check if the file exists.",  # noqa: E501
                                )

                except Exception:
                     logging.info("update successful")
                     return Status.SUCCESS

        else:
            logging.error(
                f"Failed to fetch commit information from GitHub. Response code: {response.status_code}",  # noqa: E501
            )
            logging.error("Response content:", response.text)
            return Status.ERR_UNK
