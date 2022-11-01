from npcs.soldier import Soldier

if __name__ == '__main__':
    reply = "/  7 ///  7"

    print(reply.strip("/ "))


    sold = Soldier(None, [40,40], [], None, [], [], None)
    sold.fire()
