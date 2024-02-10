from Chat import askChat,Bing
from Find import *
import asyncio
from ispBridge import IspBridge


# Edit this to change the ISPs you want to haggle with
ISPs=["Virgin media","Verizon","Vodafone","Sky"]

class Hopper:
    """Handles the haggling mainloop for each sepperate ISP being haggled with. One instance of this class is created for each ISP."""
    def __init__(self, name : str, isp : str, prices : list, address : str, callback : any=None) -> None:
        self.isp = isp
        self.name = name
        self.prices = prices
        self.address=address
        self.callback=callback
        self.IspBridge = IspBridge(isp)
        self.auto=True
        self.responceOveride=""
    async def run(self) -> None:
        """Main loop for haggling with the ISP. This is the main entry point for the haggling process. This function will run until the user overides the responce or the auto flag is set to false."""
        start="Can you help me haggle the price down with my ISP? Please say what I should message them (through their chat window not email). Put these in tripple backticks ```.    The ISP is called {} and my name is {} I live at {}. Online I found these deals you can mention {} and I want you to get me a better one."
        template="They replied: '{}'  Put your responce in tripple backticks ```  Make sure to vary the messages so they are not all the same. Before you accept the deal, get me as the client to confirm I want this deal before sending the text by including !confirm in the tripple backticks and just state the price and speed they offered (in json)."
        confirm_decline_template="{} How should I reply. Put your responce in tripple backticks ```  Make sure to not not make all the messages the same. Do not include !confirm or json in this responce."
        b=Bing()
        await b.enter()
        reply = (await askChat(b,start.format(self.isp,self.name,self.address,self.prices)))
        yield reply
        prompt = self.IspBridge.ask(reply)
        while self.auto:
            yield prompt
            prompt=template.format(prompt)
            responce = await askChat(b,prompt)
            if "!confirm" in responce or "{" in responce:
                if "{" in responce:
                    json=" ".join(" ".join(responce.replace("!confirm","").split("{")[1:]).split("}")[:-1])
                else:
                    if "£" in responce:
                        json='"price": "£'+responce.split("£")[1].split(" ")[0]+'"'
                        if "mbps" in responce:
                            json+=', "speed": "'+responce.split("mbps")[0].split(" ")[-1]+'mbps"'
                    else:
                        json=responce
                confim=self.callback.acceptDeal(json)
                # print(confirm_decline_template.format("I want to accept the deal." if confim else "I don't want to accept this deal, I want a better one."))
                responce = await askChat(b,confirm_decline_template.format("I want to accept the deal." if confim else "I don't want to accept this deal, I want a better one."))
            yield responce
            prompt = self.IspBridge.ask(responce)
        while True:
            yield prompt
            while not self.responceOveride:
                await asyncio.sleep(1)
            prompt=self.responceOveride
            yield prompt
            self.responceOveride=""
            prompt = self.IspBridge.ask(prompt)
        await b.close()



async def run():
    """Test function, only called during debugging"""
    POST_CODE="CB1 8PX"
    HOUSE_NUMBER="97"
    address = f"house number: {HOUSE_NUMBER} Postcode: {POST_CODE}"
    hoppers={}
    isps=["Virgin Media"]
    print("""
###    ###        ####          #####     #####    ###        #######
###    ###       ######        #######   #######   ###        #######     
###    ###      ###  ###       ##        ##        ###        ##
##########     ###    ###      ##  ###   ##  ###   ###        #######
###    ###    ############     ##   ##   ##   ##   ###        ##     
###    ###   ###        ###    #######   #######   ########   #######
###    ###  ###          ###    ######    ######   ########   #######

     ###    ###   #####    ######    ######    #######   ######
     ###    ###  #######   #######   #######   ##        ##   ##
     ###    ###  ##   ##   ##   ##   ##   ##   ##        ##   ##
     ##########  ##   ##   #######   #######   #######   ######
     ###    ###  ##   ##   ##        ##        ##        ## ##
     ###    ###  #######   ##        ##        ##        ##  ##
     ###    ###   #####    ##        ##        #######   ##   ##
""")
    print("Obtaining prices...")
    prices = await GetPrices(POST_CODE,HOUSE_NUMBER)
    print("Found best prices!")
    print("Starting to haggle prices down further...")
    for isp in isps:
        hoppers[isp]=Hopper("John",isp,prices,address)
    
    threads=[]
    for hopper in hoppers.values():
        threads.append(asyncio.create_task(hopper.run()))
    await asyncio.gather(*threads)

if __name__ == "__main__":
    asyncio.run(run())