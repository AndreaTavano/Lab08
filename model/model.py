from database.distributore_DAO import DistributoreDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        risultato = []

        for distributore in self._distributori:
            tutti_i_prezzi = distributore.get_prezzi()

            somma_prezzi = 0
            contatore = 0

            for prezzo in tutti_i_prezzi:
                if prezzo.data.month == mese:
                    somma_prezzi += prezzo.prezzo_litro
                    contatore += 1

            media = somma_prezzi / contatore
            risultato.append((distributore.nome, media))

        return risultato

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno == 7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente

                nuova_sequenza = []
                for tappa in sequenza_parziale:
                    nuova_sequenza.append(tappa)
                self.__sequenza_ottima = nuova_sequenza
            return

        for id_dist in prezzi_settimana:
            costo_variabile = prezzi_settimana[id_dist][giorno] * 100

            costo_fisso = 0
            if ultimo_distributore is not None and ultimo_distributore != id_dist:
                costo_fisso = 5

            nuovo_costo = costo_corrente + costo_variabile + costo_fisso

            sequenza_parziale.append(id_dist)
            self.__ricorsione(sequenza_parziale, giorno + 1, id_dist, nuovo_costo, prezzi_settimana)
            sequenza_parziale.pop()

    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        dizionario_prezzi = {}
        for distributore in self._distributori:
            prezzi_validi = []
            for prezzo in distributore.get_prezzi():
                if prezzo.data.month == mese and 1 <= prezzo.data.day <= 7:
                    prezzi_validi.append(prezzo)

            prezzi_ordinati = sorted(prezzi_validi, key=lambda p: p.data.day)

            prezzi_solo_numeri = []
            for p in prezzi_ordinati:
                prezzi_solo_numeri.append(p.prezzo_litro)

            dizionario_prezzi[distributore.id] = prezzi_solo_numeri

        return dizionario_prezzi