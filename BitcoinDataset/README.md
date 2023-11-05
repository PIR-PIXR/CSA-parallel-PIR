# Bitcoin Datasets in Real-time.

We utilized our Java code to gather 200 Bitcoin Blocks in \textit{real-time} from the \textit{latest} Block 813562, containing 2390 transactions, mined on 2023-10-24 at 09:52:26 GMT +11, to Block 813363, which included 2769 transactions and was mined on 2023-10-23 at 04:13:24 GMT +11. On average, within the dataset we collected, there were 1839 transactions in each Block. The number of transactions in each Bitcoin Block typically ranges from 1000 to 4500, and the number of active addresses per day is more than 900K. To interface with the [Blockchain Data API](https://www.blockchain.com/explorer/api/blockchain_api) for collecting real-time Bitcoin Blocks in JSON format, we used HttpURLConnection and [Google GSON](https://github.com/google/gson) 2.10.1.

## Generating Bitcoin datasets
### Installing Libraries

- #### Javac
      $ sudo apt update
      $ sudo apt upgrade
      $ sudo apt install default-jdk

### Executing MainDatasets.java
The output will generate many datasets in the Datasets folder for experimental purposes.

      $ javac -cp /path/to/BitcoinDataset/gson-2.10.1.jar:/path/to/BitcoinDataset MainDatasets.java
      $ java -cp /path/to/BitcoinDataset/gson-2.10.1.jar:/path/to/BitcoinDataset MainDatasets

### Executing MainBitcoinAPI.java
This function collects Bitcoin Blocks in real-time, and we provided many functions to interact with [Bitcoin Data API](https://www.blockchain.com/explorer/api/blockchain_api).

      $ javac -cp /path/to/BitcoinDataset/gson-2.10.1.jar:/path/to/BitcoinDataset MainBitcoinAPI.java
      $ java -cp /path/to/BitcoinDataset/gson-2.10.1.jar:/path/to/BitcoinDataset MainBitcoinAPI

---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.
