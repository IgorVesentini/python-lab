def getCalcoloDifferenza(entrata, uscita):
    # - Ora di uscita - ora di entrata
    delta = uscita - entrata
    # - Dalla differenza, ricava i minuti
    totale_minuti = int(delta.total_seconds() / 60)
    # - Calcola le ore (ricava solo i numeri interi)
    ore = totale_minuti // 60
    # - Calcola il resto
    minuti = totale_minuti % 60
    # - Formatta le ore calcolate
    ore_formattate = f"{ore}h {minuti}min"
    print("Calcolo differenza: ", ore_formattate)
    return ore_formattate
