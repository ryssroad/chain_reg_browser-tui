import concurrent.futures
from github import Github
from tqdm import tqdm
import json
import npyscreen


def read_json_from_github(content_file):
    file_content = content_file.decoded_content
    return json.loads(file_content)


def get_chain_info(subcontent, repo):
    if subcontent.name == "chain.json":
        chain_info = read_json_from_github(subcontent)
        pretty_name = chain_info.get('pretty_name')
        chain_name = chain_info.get('chain_name')
        chain_id = chain_info.get('chain_id')
        status = chain_info.get('status')
        network_type = chain_info.get('network_type')
        bech32_prefix = chain_info.get('bech32_prefix')
        slip44 = chain_info.get('slip44')
        fees = chain_info.get('fees', {}).get('fee_tokens', [{}])[0].get('denom')
        daemon_name = chain_info.get('daemon_name')
        recommended_version = chain_info.get('codebase', {}).get('recommended_version')
        website = chain_info.get('website')
        git_repo = chain_info.get('codebase', {}).get('git_repo')
        compatible_version = ', '.join(chain_info.get('codebase', {}).get('compatible_versions', []))
        # roadz testnet impl.
        # versions_recommended_version = versions[0].get('recommended_version') if versions else None
        # Получение версии и совместимых версий
        versions = chain_info.get('codebase', {}).get('versions', [])
        if versions:
            version = versions[0].get('name')
            versions_compatible_version = ', '.join(versions[0].get('compatible_versions', []))
        else:
            version = None
            versions_compatible_version = ""
        # versions_compatible_version = ', '.join(chain_info.get('codebase', {}).get('versions', [{}])[0].get('compatible_versions', []))
        versions_recommended_version = versions[0].get('recommended_version') if versions else None
        seeds = ', '.join([seed.get('address', '') for seed in chain_info.get('peers', {}).get('seeds', [])])
        persistent_peers = ', '.join([peer.get('address', '') for peer in chain_info.get('peers', {}).get('persistent_peers', [])])
        rpc = ', '.join([api.get('address', '') for api in chain_info.get('apis', {}).get('rpc', [])])
        rest = ', '.join([api.get('address', '') for api in chain_info.get('apis', {}).get('rest', [])])
        grpc = ', '.join([api.get('address', '') for api in chain_info.get('apis', {}).get('grpc', [])])
        explorers = ', '.join([explorer.get('url', '') for explorer in chain_info.get('explorers', [])])

        return {
            'pretty_name': pretty_name,
            'chain_name': chain_name,
            'chain_id': chain_id,
            'status': status,
            'network_type': network_type,
            'bech32_prefix': bech32_prefix,
            'slip44': slip44,
            'fees': fees,
            'daemon_name': daemon_name,
            'recommended_version': recommended_version,
            'website': website,
            'git_repo': git_repo,
            'compatible_version': compatible_version,
            'version': version,
            'versions_recommended_version': versions_recommended_version,

            'versions_compatible_version': versions_compatible_version,
            'seeds': seeds,
            'persistent_peers': persistent_peers,
            'rpc': rpc,
            'rest': rest,
            'grpc': grpc,
            'explorers': explorers
        }


def load_chain_info():
    # Load token from configuration file
    # with open('config.json') as json_file:
    #    data = json.load(json_file)
    TOKEN = "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"

    REPO = "cosmos/chain-registry"
    SUBDIRECTORY = "testnets"

    github = Github(TOKEN)
    # repo = REPO
    repo = github.get_repo(REPO)

    contents = repo.get_contents(SUBDIRECTORY)

    # contents = repo.get_contents("")
    chain_info_list = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for content in tqdm(contents, desc="Fetching Information", unit="repo"):
            if content.type == "dir":
                futures = [executor.submit(get_chain_info, subcontent, repo) for subcontent in repo.get_contents(content.path)]
                for future in concurrent.futures.as_completed(futures):
                    chain_info = future.result()
                    if chain_info:
                        chain_info_list.append(chain_info)

    return chain_info_list


class CustomForm(npyscreen.FormBaseNew):
    def __init__(self, chain_info_list, *args, **kwargs):
        self.chain_info_list = chain_info_list
        super().__init__(*args, **kwargs)

    def create(self):
        self.add_handlers({
            "^Q": self.exit_app
        })

        self.menu = self.add(MenuPane, relx=2, rely=2, max_width=30)
        self.menu.entry_widget.when_cursor_moved = self.update_description

        self.description = self.add(DescriptionPane, relx=34, rely=2)

        self.populate_menu()

    def populate_menu(self):
        for chain_info in self.chain_info_list:
            pretty_name = chain_info.get('pretty_name')
            self.menu.entry_widget.values.append(pretty_name)

    def update_description(self, event=None):
        selected_index = self.menu.entry_widget.cursor_line
        chain_info = self.chain_info_list[selected_index]
        self.description.update_content(chain_info)

    def exit_app(self, event):
        self.parentApp.switchForm(None)


class MenuPane(npyscreen.BoxTitle):
    def while_waiting(self):
        self.display()


class DescriptionPane(npyscreen.BoxTitle):
    def update_content(self, chain_info):
        content_list = []
        content_list.append(f"Pretty Name: {chain_info.get('pretty_name')}")
        content_list.append(f"Chain Name: {chain_info.get('chain_name')}")
        content_list.append(f"Chain ID: {chain_info.get('chain_id')}")
        content_list.append(f"Status: {chain_info.get('status')}")
        content_list.append(f"Network Type: {chain_info.get('network_type')}")
        content_list.append(f"Bech32 Prefix: {chain_info.get('bech32_prefix')}")
        content_list.append(f"Slip44: {chain_info.get('slip44')}")
        content_list.append(f"Fees: {chain_info.get('fees')}")
        content_list.append(f"Daemon Name: {chain_info.get('daemon_name')}")
        content_list.append(f"Recommended Version: {chain_info.get('recommended_version')}")
        content_list.append(f"Website: {chain_info.get('website')}")

        content_list.append(f"Git Repo: {chain_info.get('git_repo')}")
        content_list.append(f"Compatible Version: {chain_info.get('compatible_version')}")
        content_list.append(f"Version: {chain_info.get('version')}")
        content_list.append(f"Recommended Version (Versions): {chain_info.get('versions_recommended_version')}")
        content_list.append(f"Compatible Versions (Versions): {chain_info.get('versions_compatible_version')}")

        seeds = chain_info.get('seeds')
        if seeds:
            content_list.append("Seeds:")
            for seed in seeds.split(","):
                content_list.append(f"  - {seed.strip()}")

        persistent_peers = chain_info.get('persistent_peers')
        if persistent_peers:
            content_list.append("Persistent Peers:")
            for peer in persistent_peers.split(","):
                content_list.append(f"  - {peer.strip()}")

        rpc = chain_info.get('rpc')
        if rpc:
            content_list.append("RPC:")
            for api in rpc.split(","):
                content_list.append(f"  - {api.strip()}")

        rest = chain_info.get('rest')
        if rest:
            content_list.append("REST:")
            for api in rest.split(","):
                content_list.append(f"  - {api.strip()}")

        grpc = chain_info.get('grpc')
        if grpc:
            content_list.append("gRPC:")
            for api in grpc.split(","):
                content_list.append(f"  - {api.strip()}")

        explorers = chain_info.get('explorers')
        if explorers:
            content_list.append("Explorers:")
            for explorer in explorers.split(","):
                content_list.append(f"  - {explorer.strip()}")

        self.values = content_list
        self.display()


def main():
    chain_info_list_raw = load_chain_info()
    chain_info_list = [item for item in chain_info_list_raw if item.get('chain_name') != '']
    app = MyApp(chain_info_list)
    app.run()


class MyApp(npyscreen.NPSAppManaged):
    def __init__(self, chain_info_list):
        self.chain_info_list = chain_info_list
        super().__init__()

    def onStart(self):
        self.addForm("MAIN", CustomForm, name="Chain Registry", chain_info_list=self.chain_info_list)


if __name__ == "__main__":
    main()
