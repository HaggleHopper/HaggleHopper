from selenium import webdriver

class IspBridge:
    """A class to bridge the gap between the HaggleHopper and the ISP. Gets instantiated with the ISP name and then has a method to ask the ISP a question.
    This will need to be filled in with the actual code to interact with the ISP. For now it just returns a random response.
    You can use seleium for this as it gives you browser automation"""
    def __init__(self,isp):
        self.isp = isp
    def ask(self,question):
        """This method should be filled in with the actual code to interact with the ISP. For now it just returns a random response."""
        import random
        return f"I can offer you {random.randint(10,100)}mbps for £{random.randint(10,100)} per month."