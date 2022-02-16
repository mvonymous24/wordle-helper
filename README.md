# Wordle Helper
**In short, This project is a tool to help you solve wordle.**

Based on:

- 1. the analysis of the usage of thousands of 5-letter words (about 9000), 
- 2. the possibility each letter appearing on different positions, 
- 3. the colors you input, 

the program can show you the most possible answers (possibility from high to low).

![image](https://user-images.githubusercontent.com/32959489/154190189-1dda400f-3fa7-4206-a8b0-c0883e7e746b.png)


## How to use wordle helper?

### download prebuilt version

- go to `release` page, download the `.exe` file and double click it
- input one of the predicted words into [Wordle](https://www.powerlanguage.co.uk/wordle/)
- tell the program number of the word you have just input.
- tell the program colors of the word cards on Wordle. (By default, 1 means gray, 2 means yellow, 3 means green. If there's no customization, your input should be something like '**22132**')
- go back to step 2.

### or you can download sourcecode

- install python (3.9), download and run the code
- input one of the predicted words into [Wordle](https://www.powerlanguage.co.uk/wordle/)
- tell the program number of the word you have just input.
- tell the program colors of the word cards on Wordle. (By default, 1 means gray, 2 means yellow, 3 means green. If there's no customization, your input should be something like '**22132**')
- go back to step 2.

## Customize
### color code
Create a .txt file named `color_code_override.txt`, to change the color code of '1', '2', and '3'.

e.g. if the content of `color_code_override.txt` is 'abc', then you can input '**bbacb**' instead of '**22132**'

### dictionary
Find enough texts (e.g. novels, news reports, anything in multiple `.txt` files) and put them into the `dataset` folder. Create a new file named `dataset_override` and run the code.

### tip word number
Create a file named `tip_word_num_override.txt` with the content of a number larger than 5.

## Known Flaws
### Not adequately tested
This project is rough and just created for fun and practicing the usage of python language & github using. It doesn't have a pretty UI, and is not tested adequately. So literally any bug is possible. Feel free to use the code anywhere (although not recommended).

### Dictionary problem
The words provided are extracted from [an English novel dataset: txtlab_Novel450](https://figshare.com/articles/dataset/txtlab_Novel450/2062002/1). This project only contains the results of the analysis.

Wordle has a dictionary that contains every word it allows. As the dictionary this program uses is generated from the dataset, there are some words not in the Wordle dictionary (and maybe vice versa i don't know). I don't think I'm going to fix this.
