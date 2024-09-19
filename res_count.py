def res (results):
    sum_correct = 0
    n_corretti = 0
    for key, value in results.items():
        if key.count('1')==1:
            sum_correct += value
            n_corretti +=1

    print(f"Risultato corretto {sum_correct} volte, errato {1000-sum_correct}, stringhe corrette = {n_corretti}")