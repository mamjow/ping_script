import os
import time
from pythonping import ping
from datetime import datetime


class Pinging():
    """A simple ping script that store the high pings
    based on requested high value
    """
    def __init__(self):
        super().__init__()
        os.system('cls')
        self.ping_adress = input('Type the Ip adress: ')
        if not self.ping_adress:
            self.ping_adress = "4.2.2.4"
        self.ping_limit = input('type the limit: ')
        if not self.ping_limit:
            self.ping_limit = 100
        self.run = True
        self.result = {'count':0, 'high' : []}
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        with open('log.txt', 'w') as log_file:
            log_file.write(f"Pinglog start at :\t{current_time}\t limit:{self.ping_limit}ms\t ip:{self.ping_adress}\n")
        answer = None
        while answer not in ("Y", "N", "y", "n"):
            answer = input("Show log [y/n]?: ")
            if answer.lower() == "n":
                self.logging = False
            elif answer.lower() == "y":
                self.logging = True
            else:
            	print("Please enter yes or no.")

    def ip(self):
        size = os.get_terminal_size()
        p_packet=0
        l_packet =0
        while self.run:
            p_packet+=1
            test = ping(self.ping_adress, verbose=False, size=1, count=1)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.log_panel(size)

            for i in test:
                if i.success and i.time_elapsed_ms > int(self.ping_limit):
                    self.result['count'] += 1
                    self.result['high'].append((current_time , i.time_elapsed_ms))
                    with open('log.txt', 'a') as log_file:
                        log_file.write(f"{current_time}\t{i.time_elapsed_ms}\n")
                elif not i.success:
                    l_packet +=1
                    self.result['count'] += 1
                    self.result['high'].append((current_time , i.error_message))
                    with open('log.txt', 'a') as log_file:
                        log_file.write(f"{current_time}\t{i.error_message}\n")
                loss_perc = str(round( (l_packet*100)/p_packet ,2)) + "%"
                self.info_panel(size, i.time_elapsed_ms, p_packet, loss_perc)
            # self.result_panel(size)
            #time.sleep(2)

    def info_panel(self, size, avgping, p_packet, l_packet):
        print("\t{:<20}\t{:>12}".format("ping :", avgping), end="\n")
        print('*'*size[0])
        print("\t{:<20}\t{:>12}".format("Check pings for :", self.ping_adress), end="\t")
        print("\t{:<20}\t{:>12}".format("Time limit:", self.ping_limit), end="\n\n")
        print("\t{:<20}\t{:>12}".format("Packet sent:", p_packet), end="\t")
        print("\t{:<20}\t{:>12}".format("Packet loss:", l_packet), end="\n\n")
        print("\t{:<20}\t{:>12}".format("limit exceed:", str(self.result['count'])), end="\n")
        print('*'*size[0])


    def log_panel(self, size):
        os.system('cls')
        if self.logging:
            print("\t{:<6}".format("Last 10 record:"))
            print("\t{:<12}\t{:<12}".format("Time", "Ping"))
            for item in self.result['high'][-10:-1]:
                print("\t{:<12}\t{:<12}".format(str(item[0]), str(item[1])))
        print('*'*size[0])


if __name__ == '__main__':
    run = Pinging()
    run.ip()
