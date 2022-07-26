# cc-tool
Sharing all useful tool&amp;srcipt&amp;demo during my career. Enjoy !

# Usage
## 001.parse_hci_google_voice
### Requirment: 
	parse_hci_google_voice.py  
	lib_adpcm_codec.py
### Input：
	hci log
### Output:
	pcm file
### Steps:
    1.rename hci log to "btsnoop_hci.cfa"
    2.check and modify in your hci log about the parameter:TOTAL_LENGTH_1,TOTAL_LENGTH_2,DATA_HANDLE 
    3.double click parse_hci_google_voice.py 
    4.play the pcm file with（8MHZ，16bit）or（16MHZ,16bit）mono channel.
