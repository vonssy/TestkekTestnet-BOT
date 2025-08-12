from web3 import Web3
from web3.exceptions import TransactionNotFound
from eth_account import Account
from eth_abi.abi import encode
from aiohttp import ClientResponseError, ClientSession, ClientTimeout, BasicAuth
from aiohttp_socks import ProxyConnector
from datetime import datetime
from colorama import *
import asyncio, random, time, json, re, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class Testkek:
    def __init__(self) -> None:
        self.RPC_URL = "https://block-chain-testkek.alt.technology"
        self.WBTC_CONTRACT_ADDRESS = "0x12B0146068E8bC3935639e847B06c64737B34c7E"
        self.BERA_CONTRACT_ADDRESS = "0x92aEDDaBb4Eb2A5b17d90bF6fF70b58227098E03"
        self.WBERA_CONTRACT_ADDRESS = "0x89022599570c32a0754dAC2Fb5843980d15F03d3"
        self.HONEY_CONTRACT_ADDRESS = "0x0458E6a7e3F8190AaB1e7862a57f47fc4b4e0315"
        self.WETH_CONTRACT_ADDRESS = "0x8F5ecfe14FC9F1938a0C2875bfBA825C97700ADe"
        self.MULTICALL_ROUTER_ADDRESS = "0x1d0A67bb7c1afD13849C4af930dD0fD4215110fE"
        self.POSITION_ROUTER_ADDRESS = "0x5D9d05D361B191d8B81DeA40e766CEcF09327c47"
        self.QUOTER_ROUTER_ADDRESS = "0x9d08B097369d54D60461bccde45dD328c38bac8f"
        self.ERC20_CONTRACT_ABI = json.loads('''[
            {"type":"function","name":"balanceOf","stateMutability":"view","inputs":[{"name":"address","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},
            {"type":"function","name":"decimals","stateMutability":"view","inputs":[],"outputs":[{"name":"","type":"uint8"}]},
            {"type":"function","name":"allowance","stateMutability":"view","inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},
            {"type":"function","name":"approve","stateMutability":"nonpayable","inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[{"name":"","type":"bool"}]},
            {"type":"function","name":"deposit","stateMutability":"payable","inputs":[],"outputs":[]},
            {"type":"function","name":"withdraw","stateMutability":"nonpayable","inputs":[{"name":"wad","type":"uint256"}],"outputs":[]},
            {"type":"function","name":"multicall","stateMutability":"nonpayable","inputs":[{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"outputs":[{"internalType":"bytes[]","name":"","type":"bytes[]"}]}
        ]''')
        self.QUOTER_CONTRACT_ABI = [
            {
                "type": "function",
                "name": "quoteExactInput",
                "stateMutability": "nonpayable",
                "inputs": [
                    { "internalType": "bytes", "name": "path", "type": "bytes" },
                    { "internalType": "uint256", "name": "amountIn", "type": "uint256" }
                ],
                "outputs": [
                    { "internalType": "uint256", "name": "amountOut", "type": "uint256" }
                ]
            }
        ]
        self.SWAP_CONTRACT_ABI = [
            {
                "type": "function",
                "name": "multicall",
                "stateMutability": "payable",
                "inputs": [
                    { "internalType": "uint256", "name": "deadline", "type": "uint256" }, 
                    { "internalType": "bytes[]", "name": "data", "type": "bytes[]" }
                ],
                "outputs": [
                    { "internalType": "bytes[]", "name": "", "type": "bytes[]" }
                ]
            }
        ]
        self.LIQUIDITY_CONTRACT_ABI = [
            {
                "type": "function",
                "name": "multicall",
                "stateMutability": "payable",
                "inputs": [
                    { "internalType": "bytes[]", "name": "data", "type": "bytes[]" }
                ],
                "outputs": [
                    { "internalType": "bytes[]", "name": "results", "type": "bytes[]" }
                ]
            },
            {
                "type": "function",
                "name": "mint",
                "stateMutability": "nonpayable",
                "inputs": [
                    {
                        "type": "tuple",
                        "name": "params",
                        "internalType": "struct INonfungiblePositionManager.MintParams",
                        "components": [
                            { "internalType": "address", "name": "token0", "type": "address" },
                            { "internalType": "address", "name": "token1", "type": "address" },
                            { "internalType": "uint24", "name": "fee", "type": "uint24" },
                            { "internalType": "int24", "name": "tickLower", "type": "int24" },
                            { "internalType": "int24", "name": "tickUpper", "type": "int24" },
                            { "internalType": "uint256", "name": "amount0Desired", "type": "uint256" },
                            { "internalType": "uint256", "name": "amount1Desired", "type": "uint256" },
                            { "internalType": "uint256", "name": "amount0Min", "type": "uint256" },
                            { "internalType": "uint256", "name": "amount1Min", "type": "uint256" },
                            { "internalType": "address", "name": "recipient", "type": "address" },
                            { "internalType": "uint256", "name": "deadline", "type": "uint256" }
                        ]
                    }
                ],
                "outputs": [
                    { "internalType": "uint256", "name": "tokenId", "type": "uint256" },
                    { "internalType": "uint128", "name": "liquidity", "type": "uint128" },
                    { "internalType": "uint256", "name": "amount0", "type": "uint256" },
                    { "internalType": "uint256", "name": "amount1", "type": "uint256" }
                ]
            }
        ]
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.used_nonce = {}
        self.wrap_option = 0
        self.wrap_amount = 0
        self.swap_count = 0
        self.btc_swap_amount = 0
        self.wbtc_swap_amount = 0
        self.bera_swap_amount = 0
        self.wbera_swap_amount = 0
        self.honey_swap_amount = 0
        self.weth_swap_amount = 0
        self.liquidity_count = 0
        self.btc_liquidity_amount = 0
        self.wbtc_liquidity_amount = 0
        self.bera_liquidity_amount = 0
        self.wbera_liquidity_amount = 0
        self.honey_liquidity_amount = 0
        self.weth_liquidity_amount = 0
        self.min_delay = 0
        self.max_delay = 0

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Blockchain Testkek Testnet{Fore.BLUE + Style.BRIGHT} Auto BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self, use_proxy_choice: bool):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, token):
        if token not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[token] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[token]

    def rotate_proxy_for_account(self, token):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[token] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None

        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None

        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None

        raise Exception("Unsupported Proxy Type.")
    
    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address
            
            return address
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Generate Address Failed {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}                  "
            )
            return None
        
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account
        except Exception as e:
            return None
        
    def generate_swap_option(self):
        token_data = {
            "BTC": (self.WBTC_CONTRACT_ADDRESS, self.btc_swap_amount),
            "WBTC": (self.WBTC_CONTRACT_ADDRESS, self.wbtc_swap_amount),
            "BERA": (self.BERA_CONTRACT_ADDRESS, self.bera_swap_amount),
            "WBERA": (self.WBERA_CONTRACT_ADDRESS, self.wbera_swap_amount),
            "HONEY": (self.HONEY_CONTRACT_ADDRESS, self.honey_swap_amount),
            "WETH": (self.WETH_CONTRACT_ADDRESS, self.weth_swap_amount)
        }

        tickers = list(token_data.keys())

        exceptions = [
            ("WBERA", "BERA"),
            ("WBERA", "HONEY"),
            ("WBERA", "WETH"),
            ("HONEY", "WBERA"),
            ("HONEY", "WETH")
        ]

        while True:
            from_ticker = random.choice(tickers)
            to_ticker = random.choice(tickers)

            if (from_ticker, to_ticker) in exceptions:
                continue

            if from_ticker == to_ticker:
                continue

            if (from_ticker == "BTC" and to_ticker == "WBTC") or (from_ticker == "WBTC" and to_ticker == "BTC"):
                continue

            if from_ticker == "BTC":
                swap_type = "native to erc20"
            elif to_ticker == "BTC":
                swap_type = "erc20 to native"
            else:
                swap_type = "erc20 to erc20"

            from_token, amount_in = token_data[from_ticker]
            to_token, _ = token_data[to_ticker]

            return swap_type, from_ticker, to_ticker, from_token, to_token, amount_in

    def generate_liquidity_option(self):
        swap_options = [
            ("native", "BTC", "BERA", self.WBTC_CONTRACT_ADDRESS, self.BERA_CONTRACT_ADDRESS, self.btc_liquidity_amount),
            ("native", "BTC", "WBERA", self.WBTC_CONTRACT_ADDRESS, self.WBERA_CONTRACT_ADDRESS, self.btc_liquidity_amount),
            # ("native", "BTC", "HONEY", self.WBTC_CONTRACT_ADDRESS, self.HONEY_CONTRACT_ADDRESS, self.btc_liquidity_amount),
            ("native", "BTC", "WETH", self.WBTC_CONTRACT_ADDRESS, self.WETH_CONTRACT_ADDRESS, self.btc_liquidity_amount),
            ("erc20", "WBTC", "BERA", self.WBTC_CONTRACT_ADDRESS, self.BERA_CONTRACT_ADDRESS, self.wbtc_liquidity_amount),
            ("erc20", "WBTC", "WBERA", self.WBTC_CONTRACT_ADDRESS, self.WBERA_CONTRACT_ADDRESS, self.wbtc_liquidity_amount),
            ("erc20", "WBTC", "WETH", self.WBTC_CONTRACT_ADDRESS, self.WETH_CONTRACT_ADDRESS, self.wbtc_liquidity_amount),
            ("erc20", "WBERA", "BERA", self.WBERA_CONTRACT_ADDRESS, self.BERA_CONTRACT_ADDRESS, self.wbera_liquidity_amount),
            ("erc20", "WBERA", "WETH", self.WBERA_CONTRACT_ADDRESS, self.WETH_CONTRACT_ADDRESS, self.wbera_liquidity_amount),
            ("erc20", "HONEY", "WBTC", self.HONEY_CONTRACT_ADDRESS, self.WBTC_CONTRACT_ADDRESS, self.honey_liquidity_amount),
            ("erc20", "HONEY", "BERA", self.HONEY_CONTRACT_ADDRESS, self.BERA_CONTRACT_ADDRESS, self.honey_liquidity_amount),
            ("erc20", "HONEY", "WETH", self.HONEY_CONTRACT_ADDRESS, self.WETH_CONTRACT_ADDRESS, self.honey_liquidity_amount),
            ("erc20", "WETH", "BERA", self.WETH_CONTRACT_ADDRESS, self.BERA_CONTRACT_ADDRESS, self.weth_liquidity_amount)
        ]

        token_type, ticker0, ticker1, token0, token1, amount0 = random.choice(swap_options)

        liquidity_option = f"{ticker0}/{ticker1}"

        amount0_desired = int(amount0 * (10 ** 18))

        return liquidity_option, token_type, ticker0, ticker1, token0, token1, amount0_desired
        
    async def get_web3_with_check(self, address: str, use_proxy: bool, retries=3, timeout=60):
        request_kwargs = {"timeout": timeout}

        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        if use_proxy and proxy:
            request_kwargs["proxies"] = {"http": proxy, "https": proxy}

        for attempt in range(retries):
            try:
                web3 = Web3(Web3.HTTPProvider(self.RPC_URL, request_kwargs=request_kwargs))
                web3.eth.get_block_number()
                return web3
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                raise Exception(f"Failed to Connect to RPC: {str(e)}")
            
    async def send_raw_transaction_with_retries(self, account, web3, tx, retries=5):
        for attempt in range(retries):
            try:
                signed_tx = web3.eth.account.sign_transaction(tx, account)
                raw_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                tx_hash = web3.to_hex(raw_tx)
                return tx_hash
            except TransactionNotFound:
                pass
            except Exception as e:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} [Attempt {attempt + 1}] Send TX Error: {str(e)} {Style.RESET_ALL}"
                )
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Hash Not Found After Maximum Retries")

    async def wait_for_receipt_with_retries(self, web3, tx_hash, retries=5):
        for attempt in range(retries):
            try:
                receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
                return receipt
            except TransactionNotFound:
                pass
            except Exception as e:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} [Attempt {attempt + 1}] Wait for Receipt Error: {str(e)} {Style.RESET_ALL}"
                )
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Receipt Not Found After Maximum Retries")
        
    async def get_token_balance(self, address: str, contract_address: str, use_proxy: bool, retries=5):
        for attempt in range(retries):
            try:
                web3 = await self.get_web3_with_check(address, use_proxy)

                if contract_address == "BTC":
                    balance = web3.eth.get_balance(address)
                    decimals = 18
                else:
                    token_contract = web3.eth.contract(address=web3.to_checksum_address(contract_address), abi=self.ERC20_CONTRACT_ABI)
                    balance = token_contract.functions.balanceOf(address).call()
                    decimals = token_contract.functions.decimals().call()

                token_balance = balance / (10 ** decimals)

                return token_balance
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                return None
        
    async def perform_wrapped(self, account: str, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            contract_address = web3.to_checksum_address(self.WBTC_CONTRACT_ADDRESS)
            token_contract = web3.eth.contract(address=contract_address, abi=self.ERC20_CONTRACT_ABI)

            amount_to_wei = web3.to_wei(self.wrap_amount, "ether")
            wrap_data = token_contract.functions.deposit()
            estimated_gas = wrap_data.estimate_gas({"from":address, "value":amount_to_wei})

            max_priority_fee = web3.to_wei(0.1, "gwei")
            max_fee = max_priority_fee

            wrap_tx = wrap_data.build_transaction({
                "from": address,
                "value": amount_to_wei,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": self.used_nonce[address],
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, wrap_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber
            self.used_nonce[address] += 1

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None, None
        
    async def perform_unwrapped(self, account: str, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            contract_address = web3.to_checksum_address(self.WBTC_CONTRACT_ADDRESS)
            token_contract = web3.eth.contract(address=contract_address, abi=self.ERC20_CONTRACT_ABI)

            amount_to_wei = web3.to_wei(self.wrap_amount, "ether")
            unwrap_data = token_contract.functions.withdraw(amount_to_wei)
            estimated_gas = unwrap_data.estimate_gas({"from":address})

            max_priority_fee = web3.to_wei(0.1, "gwei")
            max_fee = max_priority_fee

            unwrap_tx = unwrap_data.build_transaction({
                "from": address,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": self.used_nonce[address],
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, unwrap_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber
            self.used_nonce[address] += 1

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None, None
        
    async def get_amount_out_min(self, address: str, path: str, amount_in_wei: int, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            contract = web3.eth.contract(address=web3.to_checksum_address(self.QUOTER_ROUTER_ADDRESS), abi=self.QUOTER_CONTRACT_ABI)

            amount_out = contract.functions.quoteExactInput(path, amount_in_wei).call()
            
            return amount_out
        except Exception as e:
            return None
        
    async def approving_token(self, account: str, address: str, router_address: str, asset_address: str, amount_to_wei: int, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)
            
            spender = web3.to_checksum_address(router_address)
            token_contract = web3.eth.contract(address=web3.to_checksum_address(asset_address), abi=self.ERC20_CONTRACT_ABI)

            allowance = token_contract.functions.allowance(address, spender).call()
            if allowance < amount_to_wei:
                approve_data = token_contract.functions.approve(spender, 2**256 - 1)
                estimated_gas = approve_data.estimate_gas({"from": address})

                max_priority_fee = web3.to_wei(0.1, "gwei")
                max_fee = max_priority_fee

                approve_tx = approve_data.build_transaction({
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id,
                })

                tx_hash = await self.send_raw_transaction_with_retries(account, web3, approve_tx)
                receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
                block_number = receipt.blockNumber
                self.used_nonce[address] += 1

                explorer = f"https://explorer.block-chain.lol/tx/{tx_hash}"
                
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}   Approve  :{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}   Block    :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}   Tx Hash  :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}   Explorer :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {explorer} {Style.RESET_ALL}"
                )
                await self.print_timer()

            return True
        except Exception as e:
            raise Exception(f"Approving Token Contract Failed: {str(e)}")
        
    def generate_multicall_bytes_data(self, address: str, swap_type: str, fee: int, from_token: str, to_token: str, amount_in_wei: int, amount_out_min_wei: int):
        try:
            if swap_type in ["native to erc20", "erc20 to erc20"]:
                exact_input_single_prefix = bytes.fromhex('04e45aaf')
                exact_input_single_bytes = encode(
                    ['address', 'address', 'uint24', 'address', 'uint256', 'uint256', 'uint160'],
                    [
                        from_token,
                        to_token,
                        fee,
                        address,
                        amount_in_wei,
                        amount_out_min_wei,
                        0
                    ]
                )
            
                data_bytes = [exact_input_single_prefix + exact_input_single_bytes]

            elif swap_type == "erc20 to native":
                exact_input_single_prefix = bytes.fromhex('04e45aaf')
                exact_input_single_bytes = encode(
                    ['address', 'address', 'uint24', 'address', 'uint256', 'uint256', 'uint160'],
                    [
                        from_token,
                        to_token,
                        fee,
                        "0x0000000000000000000000000000000000000002",
                        amount_in_wei,
                        amount_out_min_wei,
                        0
                    ]
                )

                unwrap_weth_9_prefix = bytes.fromhex('49404b7c')
                unwrap_weth_9_bytes = encode(
                    ['uint256', 'address'],
                    [
                        amount_out_min_wei,
                        address
                    ]
                )
                
                data_bytes = [exact_input_single_prefix + exact_input_single_bytes, unwrap_weth_9_prefix +unwrap_weth_9_bytes ]

            return data_bytes
        except Exception as e:
            raise Exception(f"Generate Multicall Bytes Data Failed: {str(e)}")
        
    async def perform_swap(self, account: str, address: str, swap_type: str, from_token: str, to_token: str, amount_in: float, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            amount_in_wei = web3.to_wei(amount_in, "ether")

            exceptions = [
                (self.BERA_CONTRACT_ADDRESS, self.WETH_CONTRACT_ADDRESS),
                (self.WETH_CONTRACT_ADDRESS, self.BERA_CONTRACT_ADDRESS)
            ]

            fee = 500 if swap_type == "erc20 to native" or (from_token, to_token) in exceptions else 3000

            if swap_type != "native to erc20":
                await self.approving_token(account, address, self.MULTICALL_ROUTER_ADDRESS, from_token, amount_in_wei, use_proxy)

            path = bytes.fromhex(from_token[2:]) + (fee).to_bytes(3, "big") + bytes.fromhex(to_token[2:])

            amount_out_wei = await self.get_amount_out_min(address, path, amount_in_wei, use_proxy)
            if not amount_out_wei:
                raise Exception("Fetch Amount Out Min Failed")
            
            amount_out_min_wei = (amount_out_wei * (10000 - 10)) // 10000

            deadline = int(time.time()) + 600

            data_bytes = self.generate_multicall_bytes_data(address, swap_type, fee, from_token, to_token, amount_in_wei, amount_out_min_wei)

            max_priority_fee = web3.to_wei(0.1, "gwei")
            max_fee = max_priority_fee

            if swap_type == "native to erc20":
                token_contract = web3.eth.contract(address=web3.to_checksum_address(self.MULTICALL_ROUTER_ADDRESS), abi=self.SWAP_CONTRACT_ABI)
                swap_data = token_contract.functions.multicall(deadline, data_bytes)
                estimated_gas = swap_data.estimate_gas({"from": address, "value":amount_in_wei})
                swap_tx = swap_data.build_transaction({
                    "from": address,
                    "value": amount_in_wei,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id
                })

            else:
                token_contract = web3.eth.contract(address=web3.to_checksum_address(self.MULTICALL_ROUTER_ADDRESS), abi=self.ERC20_CONTRACT_ABI)
                swap_data = token_contract.functions.multicall(deadline, data_bytes)
                estimated_gas = swap_data.estimate_gas({"from": address})
                swap_tx = swap_data.build_transaction({
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id
                })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, swap_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber
            self.used_nonce[address] += 1

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None, None
        
    def generate_liquidity_calldata(self, address: str, token_type: str, token0: str, token1: str, amount0_desired: int, amount1_desired: int):
        try:
            amount0_min = (amount0_desired * (10000 - 100)) // 10000
            amount1_min = (amount1_desired * (10000 - 100)) // 10000
            deadline = int(time.time()) + 600

            if token_type == "native":
                mint_prefix = bytes.fromhex("88316456")
                mint_params = encode(
                    [
                        'address', 'address', 'uint24', 'int24', 'int24', 'uint256', 
                        'uint256', 'uint256', 'uint256', 'address', 'uint256'
                    ],
                    [
                        token0, token1, 3000, -887220, 887220, amount0_desired,
                        amount1_desired, amount0_min, amount1_min, address, deadline
                    ]
                )
                refund_eth_prefix = bytes.fromhex("12210e8a")

                calldata = [mint_prefix + mint_params, refund_eth_prefix]

            elif token_type == "erc20":
                calldata = (
                    token0, token1, 3000, -887220, 887220, amount0_desired, 
                    amount1_desired, amount0_min, amount1_min, address, deadline
                )

            return calldata
        except Exception as e:
            raise Exception(f"Generate Liquidity Calldata Failed: {str(e)}")
        
    async def perform_liquidity(self, account: str, address: str, token_type: str, token0: str, token1: str, amount0_desired: int, amount1_desired: int, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)
            
            await self.approving_token(account, address, self.POSITION_ROUTER_ADDRESS, token1, amount1_desired, use_proxy)

            if token_type == "erc20":
                await self.approving_token(account, address, self.POSITION_ROUTER_ADDRESS, token0, amount0_desired, use_proxy)

            token_contract = web3.eth.contract(address=web3.to_checksum_address(self.POSITION_ROUTER_ADDRESS), abi=self.LIQUIDITY_CONTRACT_ABI)

            calldata = self.generate_liquidity_calldata(address, token_type, token0, token1, amount0_desired, amount1_desired)

            max_priority_fee = web3.to_wei(0.1, "gwei")
            max_fee = max_priority_fee

            if token_type == "native":
                liquidity_data = token_contract.functions.multicall(calldata)
                estimated_gas = liquidity_data.estimate_gas({"from": address, "value":amount1_desired})
                liquidity_tx = liquidity_data.build_transaction({
                    "from": address,
                    "value": amount1_desired,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id
                })

            elif token_type == "erc20":
                liquidity_data = token_contract.functions.mint(calldata)
                estimated_gas = liquidity_data.estimate_gas({"from": address})
                liquidity_tx = liquidity_data.build_transaction({
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id
                })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, liquidity_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber
            self.used_nonce[address] += 1

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Message  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None, None
        
    def print_wrap_question(self):
        while True:
            try:
                wrap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter BTC Amount -> {Style.RESET_ALL}").strip())
                if wrap_amount > 0:
                    self.wrap_amount = wrap_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}BTC Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")
    
    def print_unwrap_question(self):
        while True:
            try:
                wrap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter WBTC Amount -> {Style.RESET_ALL}").strip())
                if wrap_amount > 0:
                    self.wrap_amount = wrap_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}WBTC Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

    def print_wrap_or_unwarp_option(self):
        while True:
            try:
                print(f"{Fore.GREEN + Style.BRIGHT}Select Option:{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}1. Wrap BTC{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Unwrap WBTC{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Skipped{Style.RESET_ALL}")
                wrap_option = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if wrap_option in [1, 2, 3]:
                    wrap_type = (
                        "Wrap BTC" if wrap_option == 1 else 
                        "Unwrap WBTC" if wrap_option == 2 else 
                        "Skipped"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{wrap_type} Selected.{Style.RESET_ALL}")
                    self.wrap_option = wrap_option

                    if self.wrap_option == 1:
                        self.print_wrap_question()
                    elif self.wrap_option == 2:
                        self.print_unwrap_question()

                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

    def print_swap_question(self):
        while True:
            try:
                swap_count = int(input(f"{Fore.YELLOW + Style.BRIGHT}Swap Count For Each Wallet -> {Style.RESET_ALL}").strip())
                if swap_count > 0:
                    self.swap_count = swap_count
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Swap Count must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        while True:
            try:
                btc_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter BTC Swap Amount -> {Style.RESET_ALL}").strip())
                if btc_swap_amount > 0:
                    self.btc_swap_amount = btc_swap_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}BTC Swap Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                wbtc_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter WBTC Swap Amount -> {Style.RESET_ALL}").strip())
                if wbtc_swap_amount > 0:
                    self.wbtc_swap_amount = wbtc_swap_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}WBTC Swap Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                bera_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter BERA Swap Amount -> {Style.RESET_ALL}").strip())
                if bera_swap_amount > 0:
                    self.bera_swap_amount = bera_swap_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}BERA Swap Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                wbera_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter WBERA Swap Amount -> {Style.RESET_ALL}").strip())
                if wbera_swap_amount > 0:
                    self.wbera_swap_amount = wbera_swap_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}WBERA Swap Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                honey_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter HONEY Swap Amount -> {Style.RESET_ALL}").strip())
                if honey_swap_amount > 0:
                    self.honey_swap_amount = honey_swap_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}HONEY Swap Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                weth_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter WETH Swap Amount -> {Style.RESET_ALL}").strip())
                if weth_swap_amount > 0:
                    self.weth_swap_amount = weth_swap_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}WETH Swap Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

    def print_liquidity_question(self):
        while True:
            try:
                liquidity_count = int(input(f"{Fore.YELLOW + Style.BRIGHT}Add Liquidity Count For Each Wallet -> {Style.RESET_ALL}").strip())
                if liquidity_count > 0:
                    self.liquidity_count = liquidity_count
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Add Liquidity Count must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        while True:
            try:
                btc_liquidity_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter BTC Liquidity Amount -> {Style.RESET_ALL}").strip())
                if btc_liquidity_amount > 0:
                    self.btc_liquidity_amount = btc_liquidity_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}BTC Liquidity Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                wbtc_liquidity_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter WBTC Liquidity Amount -> {Style.RESET_ALL}").strip())
                if wbtc_liquidity_amount > 0:
                    self.wbtc_liquidity_amount = wbtc_liquidity_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}WBTC Liquidity Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                bera_liquidity_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter BERA Liquidity Amount -> {Style.RESET_ALL}").strip())
                if bera_liquidity_amount > 0:
                    self.bera_liquidity_amount = bera_liquidity_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}BERA Liquidity Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                wbera_liquidity_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter WBERA Liquidity Amount -> {Style.RESET_ALL}").strip())
                if wbera_liquidity_amount > 0:
                    self.wbera_liquidity_amount = wbera_liquidity_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}WBERA Liquidity Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                honey_liquidity_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter HONEY Liquidity Amount -> {Style.RESET_ALL}").strip())
                if honey_liquidity_amount > 0:
                    self.honey_liquidity_amount = honey_liquidity_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}HONEY Liquidity Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        while True:
            try:
                weth_liquidity_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter WETH Liquidity Amount -> {Style.RESET_ALL}").strip())
                if weth_liquidity_amount > 0:
                    self.weth_liquidity_amount = weth_liquidity_amount
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}WETH Liquidity Amount must be > 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

    def print_delay_question(self):
        while True:
            try:
                min_delay = int(input(f"{Fore.YELLOW + Style.BRIGHT}Min Delay For Each Tx -> {Style.RESET_ALL}").strip())
                if min_delay >= 0:
                    self.min_delay = min_delay
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Min Delay must be >= 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        while True:
            try:
                max_delay = int(input(f"{Fore.YELLOW + Style.BRIGHT}Max Delay For Each Tx -> {Style.RESET_ALL}").strip())
                if max_delay >= min_delay:
                    self.max_delay = max_delay
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Max Delay must be >= Min Delay.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")
         
    async def print_timer(self):
        for remaining in range(random.randint(self.min_delay, self.max_delay), 0, -1):
            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Wait For{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Seconds For Next Tx...{Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            await asyncio.sleep(1)

    def print_question(self):
        while True:
            try:
                print(f"{Fore.GREEN + Style.BRIGHT}Select Option:{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}1. Wrap BTC{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Unwrap WBTC{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Random Swap{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}4. Add Liquidity{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}5. Run All Features{Style.RESET_ALL}")
                option = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3/4/5] -> {Style.RESET_ALL}").strip())

                if option in [1, 2, 3, 4, 5]:
                    option_type = (
                        "Wrap BTC" if option == 1 else 
                        "Unwrap WBTC" if option == 2 else 
                        "Random Swap" if option == 3 else
                        "Add Liquidity" if option == 4 else
                        "Run All Features"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{option_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2, 3, 4, or 5.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2, 3, 4, or 5).{Style.RESET_ALL}")

        if option == 1:
            self.print_wrap_question()
            self.print_delay_question()

        elif option == 2:
            self.print_unwrap_question()
            self.print_delay_question()

        elif option == 3:
            self.print_swap_question()
            self.print_delay_question()

        elif option == 4:
            self.print_liquidity_question()
            self.print_delay_question()

        elif option == 5:
            self.print_wrap_or_unwarp_option()
            self.print_swap_question()
            self.print_liquidity_question()
            self.print_delay_question()

        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Free Proxyscrape" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return option, choose, rotate
    
    async def check_connection(self, proxy_url=None):
        connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=10)) as session:
                async with session.get(url="https://api.ipify.org?format=json", proxy=proxy, proxy_auth=proxy_auth) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError) as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status    :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Connection Not 200 OK {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None
    
    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy     :{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )

            is_valid = await self.check_connection(proxy)
            if not is_valid:
                if rotate_proxy:
                    proxy = self.rotate_proxy_for_account(address)
                    continue

                return False
            
            return True
        
    async def process_perform_wrapped(self, account: str, address: str, use_proxy: bool):
        tx_hash, block_number = await self.perform_wrapped(account, address, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://explorer.block-chain.lol/tx/{tx_hash}"
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Block    :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Tx Hash  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Explorer :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {explorer} {Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Perform On-Chain Failed {Style.RESET_ALL}"
            )

    async def process_perform_unwrapped(self, account: str, address: str, use_proxy: bool):
        tx_hash, block_number = await self.perform_unwrapped(account, address, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://explorer.block-chain.lol/tx/{tx_hash}"
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Block    :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Tx Hash  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Explorer :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {explorer} {Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Perform On-Chain Failed {Style.RESET_ALL}"
            )

    async def process_perform_swap(self, account: str, address: str, swap_type: str, from_token: str, to_token: str, amount_in: float, use_proxy: bool):
        tx_hash, block_number = await self.perform_swap(account, address, swap_type, from_token, to_token, amount_in, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://explorer.block-chain.lol/tx/{tx_hash}"
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Block    :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Tx Hash  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Explorer :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {explorer} {Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Perform On-Chain Failed {Style.RESET_ALL}"
            )

    async def process_perform_liquidity(self, account: str, address: str, token_type: str, token0: str, token1: str, amount0_desired: int, amount1_desired: int, use_proxy: bool):
        tx_hash, block_number = await self.perform_liquidity(account, address, token_type, token0, token1, amount0_desired, amount1_desired, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://explorer.block-chain.lol/tx/{tx_hash}"
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Block    :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Tx Hash  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Explorer :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {explorer} {Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Perform On-Chain Failed {Style.RESET_ALL}"
            )

    async def process_option_1(self, account: str, address: str, use_proxy):
        self.log(f"{Fore.CYAN+Style.BRIGHT}Wrapped   :{Style.RESET_ALL}                      ")

        balance = await self.get_token_balance(address, "BTC", use_proxy)
        self.log(
            f"{Fore.CYAN+Style.BRIGHT}   Balance :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {balance} BTC {Style.RESET_ALL}"
        )
        self.log(
            f"{Fore.CYAN+Style.BRIGHT}   Amount  :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {self.wrap_amount} BTC {Style.RESET_ALL}"
        )

        if not balance or balance <=  self.wrap_amount:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} Insufficient BTC Token Balance {Style.RESET_ALL}"
            )
            return
        
        await self.process_perform_wrapped(account, address, use_proxy)

    async def process_option_2(self, account: str, address: str, use_proxy):
        self.log(f"{Fore.CYAN+Style.BRIGHT}Unwrapped :{Style.RESET_ALL}                      ")

        balance = await self.get_token_balance(address, self.WBTC_CONTRACT_ADDRESS, use_proxy)
        self.log(
            f"{Fore.CYAN+Style.BRIGHT}   Balance  :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {balance} WBTC {Style.RESET_ALL}"
        )
        self.log(
            f"{Fore.CYAN+Style.BRIGHT}   Amount   :{Style.RESET_ALL}"
            f"{Fore.WHITE+Style.BRIGHT} {self.wrap_amount} WBTC {Style.RESET_ALL}"
        )

        if not balance or balance <=  self.wrap_amount:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} Insufficient WBTC Token Balance {Style.RESET_ALL}"
            )
            return
        
        await self.process_perform_unwrapped(account, address, use_proxy)

    async def process_option_3(self, account: str, address: str, use_proxy):
        self.log(f"{Fore.CYAN+Style.BRIGHT}Swap      :{Style.RESET_ALL}                      ")
        for i in range(self.swap_count):
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}Swap{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {i+1} / {self.swap_count} {Style.RESET_ALL}                           "
            )

            swap_type, from_ticker, to_ticker, from_token, to_token, amount_in = self.generate_swap_option()

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Option   :{Style.RESET_ALL}"
                f"{Fore.BLUE+Style.BRIGHT} {from_ticker} to {to_ticker} {Style.RESET_ALL}"
            )

            if swap_type != "native to erc20":
                balance = await self.get_token_balance(address, from_token, use_proxy)
            else:
                balance = await self.get_token_balance(address, "BTC", use_proxy)

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Balance  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {balance} {from_ticker} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Amount   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {amount_in} {from_ticker} {Style.RESET_ALL}"
            )

            if not balance or balance <=  amount_in:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient {from_ticker} Token Balance {Style.RESET_ALL}"
                )
                continue
            
            await self.process_perform_swap(account, address, swap_type, from_token, to_token, amount_in, use_proxy)
            await self.print_timer()

    async def process_option_4(self, account: str, address: str, use_proxy):
        self.log(f"{Fore.CYAN+Style.BRIGHT}Liquidity :{Style.RESET_ALL}                      ")
        for i in range(self.liquidity_count):
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT} ● {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}Liquidity{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {i+1} / {self.liquidity_count} {Style.RESET_ALL}                           "
            )

            liquidity_option, token_type, ticker0, ticker1, token0, token1, amount0_desired = self.generate_liquidity_option()

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}   Option   :{Style.RESET_ALL}"
                f"{Fore.BLUE+Style.BRIGHT} {liquidity_option} {Style.RESET_ALL}"
            )

            if token_type == "native":
                balance0 = await self.get_token_balance(address, "BTC", use_proxy)

            elif token_type == "erc20":
                balance0 = await self.get_token_balance(address, token0, use_proxy)
            
            balance1 = await self.get_token_balance(address, token1, use_proxy)

            self.log(f"{Fore.CYAN+Style.BRIGHT}   Balance  :{Style.RESET_ALL}")
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{balance0} {ticker0}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{balance1} {ticker1}{Style.RESET_ALL}"
            )

            path = bytes.fromhex(token0[2:]) + (3000).to_bytes(3, "big") + bytes.fromhex(token1[2:])
            amount1_desired = await self.get_amount_out_min(address, path, amount0_desired, use_proxy)
            if not amount1_desired:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Fetch {ticker0} per {ticker1} Current Price Failed {Style.RESET_ALL}"
                )
                continue

            amount0 = amount0_desired / (10 ** 18)
            amount1 = amount1_desired / (10 ** 18)

            self.log(f"{Fore.CYAN+Style.BRIGHT}   Amount   :{Style.RESET_ALL}")
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{amount0} {ticker0}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}      ● {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{amount1} {ticker1}{Style.RESET_ALL}"
            )

            if not balance0 or balance0 <=  amount0:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient {ticker0} Token Balance {Style.RESET_ALL}"
                )
                continue
            
            if not balance1 or balance1 <=  amount1:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}   Status   :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient {ticker1} Token Balance {Style.RESET_ALL}"
                )
                continue
            
            await self.process_perform_liquidity(account, address, token_type, token0, token1, amount0_desired, amount1_desired, use_proxy)
            await self.print_timer()

    async def process_accounts(self, account: str, address: str, option: int, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(address, use_proxy, rotate_proxy)
        if is_valid:
            try:
                web3 = await self.get_web3_with_check(address, use_proxy)
            except Exception as e:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Web3 Not Connected {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                return
            
            self.used_nonce[address] = web3.eth.get_transaction_count(address, "pending")
            
            if option == 1:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Option    :{Style.RESET_ALL}"
                    f"{Fore.BLUE+Style.BRIGHT} Wrap UOMI {Style.RESET_ALL}"
                )
                await self.process_option_1(account, address, use_proxy)

            elif option == 2:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Option    :{Style.RESET_ALL}"
                    f"{Fore.BLUE+Style.BRIGHT} Unwrap WUOMI {Style.RESET_ALL}"
                )
                await self.process_option_2(account, address, use_proxy)

            elif option == 3:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Option    :{Style.RESET_ALL}"
                    f"{Fore.BLUE+Style.BRIGHT} Random Swap {Style.RESET_ALL}"
                )
                await self.process_option_3(account, address, use_proxy)

            elif option == 4:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Option    :{Style.RESET_ALL}"
                    f"{Fore.BLUE+Style.BRIGHT} Add Liquidity {Style.RESET_ALL}"
                )
                await self.process_option_4(account, address, use_proxy)

            elif option == 5:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Option    :{Style.RESET_ALL}"
                    f"{Fore.BLUE+Style.BRIGHT} Run All Features {Style.RESET_ALL}"
                )

                if self.wrap_option == 1:
                    await self.process_option_1(account, address, use_proxy)
                elif self.wrap_option == 2:
                    await self.process_option_2(account, address, use_proxy)

                await asyncio.sleep(5)

                await self.process_option_3(account, address, use_proxy)
                await asyncio.sleep(5)

                await self.process_option_4(account, address, use_proxy)
                await asyncio.sleep(5)

    async def main(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]

            option, use_proxy_choice, rotate_proxy = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
                )

                if use_proxy:
                    await self.load_proxies(use_proxy_choice)
                
                separator = "=" * 25
                for account in accounts:
                    if account:
                        address = self.generate_address(account)

                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )

                        if not address:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}Status    :{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Invalid Private Key or Library Version Not Supported {Style.RESET_ALL}"
                            )
                            continue

                        await self.process_accounts(account, address, option, use_proxy_choice, rotate_proxy)
                        await asyncio.sleep(3)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*72)
                seconds = 1 * 60 * 60
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed.{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Testkek()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Blockchain Testkek Testnet - BOT{Style.RESET_ALL}                                       "                              
        )