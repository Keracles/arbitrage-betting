import pickle

bookmaker = "unibet"
bookmakers = ["unibet", "winamax", "netbet", "betclic", "netbet"]
creation = False
creation_all = False

if creation :
    pickle_out = open(f'bookmakers\\trad_bookmakers\\{bookmaker}.pkl',"wb")
    pickle.dump({}, pickle_out)
    pickle_out.close()

with open(f'bookmakers\\trad_bookmakers\\{bookmaker}.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)
    f.close()

print(loaded_dict)


if creation_all:
    for bookmaker in bookmakers:
        pickle_out = open(f'bookmakers\\trad_bookmakers\\{bookmaker}.pkl',"wb")
        pickle.dump({}, pickle_out)
        pickle_out.close()

        with open(f'bookmakers\\trad_bookmakers\\{bookmaker}.pkl', 'rb') as f:
            loaded_dict = pickle.load(f)
            f.close()
        print(loaded_dict)