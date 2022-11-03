import pickle

bookmaker = "netbet"
creation = True

if creation :
    pickle_out = open(f'bookmakers\\trad_bookmakers\\{bookmaker}.pkl',"wb")
    pickle.dump({}, pickle_out)
    pickle_out.close()

with open(f'bookmakers\\trad_bookmakers\\{bookmaker}.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)
    f.close()

print(loaded_dict)


