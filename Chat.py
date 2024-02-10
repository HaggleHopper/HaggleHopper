import asyncio
from sydney import SydneyClient

class Bing:
    """This is code that uses a modified version of the Sydeny library in order to interact with the Bing chatbot."""
    def __init__(self) -> None:
        self.die=False # This is a flag to tell the chatbot to stop
        # Create a new instance of the SydneyClient with the bing_u_cookie set to the value of the cookie you got from the Bing chatbot (If Microsoft reset the cookie, you will need to get a new one from the Bing chatbot)
        self.sydney=SydneyClient(bing_u_cookie= "1scZqEuvQazNDG15lRwi2Qu81G6cXfujIBjhl_aoe_Mqdie7kZ_cqQAhQhUuvQPCsXCYXynh5tnAJa36959_UF2uyk_A_IP55kAdOqEvOTRPdevUFE40KuTlcx0dFQndbm8W57L8Of7bSaWIrDfdWt4czekU7xCNBSghxeheC_p6U3-BFOHAXx88zy1eYghIsBsh7JZwa1nNwPAq2xfTwVqQgEaiW25UDvPURFf4Bd9Q")
    
    async def enter(self):
        await self.sydney.__aenter__()

    async def close(self):
        await self.sydney.__aexit__(None,None,None)

    async def askChat(self,prompt) -> None:
        """Ask the chatbot a question and return the response. If the prompt is "!reset" then reset the conversation with the chatbot."""
        self.responce=""
        if prompt == "!reset":
            await self.sydney.reset_conversation()
            return
        async for response in self.sydney.ask_stream(prompt):
            if response:
                self.responce=response
            if self.responce=="Captcha required":
                print("Captcha required, this is not meant to happen. Please log in manually and get a new cookie. If this keeps happening, Microsoft may have changed the way the chatbot works and so contact a Developer.")
        return self.responce

template="They replied: '{}'  Put your responce in tripple backticks ```"
start="Can you help me haggle the price down with my ISP? Please say what I should message them. Put these in tripple backticks ```.    The ISP is called {} and my name is {}"

isp="Virgin media"
name="John"


"""
email:HaggleHopperDemo1@outlook.com
password:HaggleHopperSeleniumD1
"""


async def askChat(b,prompt):
    res=""
    for _ in range(3): # 3 attempts to get bing to work
        res=await b.askChat(prompt)
        if "```" in res:
            return res.split("```")[1].replace("**","")
    raise Exception("Bing failed to respond in correct format:  "+res)

async def run():
    """This is a test function used in debugging. It will ask the chatbot a question and then print the responce. It will then ask the user for a prompt and print the responce. This will continue until the user types "!exit"."""
    b=Bing()
    await b.enter()
    print(await askChat(b,start.format(isp,name)))
    x = input("Enter a prompt: ")
    while x!="!exit":
        x=template.format(x)
        print(await askChat(b,x))
        x = input("Enter a prompt: ")
    await b.close()

if __name__ == "__main__":
    asyncio.run(run())


    
