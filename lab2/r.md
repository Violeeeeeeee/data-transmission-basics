# 2.1

## a.

### 1. Zrozumienie elementów wzoru

Twój sygnał jest zdefiniowany jako:
$$x(n)=\sum_{k=0}^{\infty}(-1)^{k}\delta(n-3k)$$

Rozbijmy go na trzy kluczowe części:
* **$\delta(n-3k)$**: Jest to dyskretna funkcja impulsowa (często nazywana deltą Kroneckera, a w inżynierii deltą Diraca dla czasu dyskretnego). Jej zasada działania jest prosta: przyjmuje wartość **$1$**, gdy jej argument wynosi zero (czyli gdy $n-3k=0$, co daje $n=3k$). Dla wszystkich innych wartości przyjmuje **$0$**. Zatem $\delta(n-3k)$ to pojedynczy "prążek" pojawiający się tylko w chwili $n = 3k$.
* **$(-1)^k$**: To amplituda (wysokość) danego prążka. Ponieważ potęgujemy liczbę ujemną, wartość ta będzie naprzemiennie wynosić **$1$** (dla $k$ parzystych, np. 0, 2, 4) oraz **$-1$** (dla $k$ nieparzystych, np. 1, 3, 5).
* **$\sum_{k=0}^{\infty}$**: Znak sumy oznacza, że sygnał $x(n)$ to po prostu zbiór wszystkich tych prążków dodanych do siebie, zaczynając od $k=0$ aż do nieskończoności.

### 2. Rozpisanie pierwszych wyrazów sumy
Najlepszym sposobem na wizualizację takiego sygnału jest podstawienie kilku pierwszych wartości $k$:

* Dla **$k = 0$**: $(-1)^0\delta(n-3\cdot0) = \mathbf{1\cdot\delta(n)}$
    * *Oznacza to prążek o wysokości $1$ w punkcie $n=0$.*
* Dla **$k = 1$**: $(-1)^1\delta(n-3\cdot1) = \mathbf{-1\cdot\delta(n-3)}$
    * *Oznacza to prążek o wysokości $-1$ w punkcie $n=3$.*
* Dla **$k = 2$**: $(-1)^2\delta(n-3\cdot2) = \mathbf{1\cdot\delta(n-6)}$
    * *Oznacza to prążek o wysokości $1$ w punkcie $n=6$.*
* Dla **$k = 3$**: $(-1)^3\delta(n-3\cdot3) = \mathbf{-1\cdot\delta(n-9)}$
    * *Oznacza to prążek o wysokości $-1$ w punkcie $n=9$.*

Sygnał "skacze" między wartościami 1 a -1 i pojawia się co trzecią próbkę. Dla wszystkich pozostałych wartości $n$ (np. $n=1, 2, 4, 5, 7, 8$ itd.) wartość sygnału wynosi **zero**. Ponieważ sumowanie zaczyna się od $k=0$, to dla wszystkich ujemnych wartości $n$ (np. $n=-1, -2, -3$) sygnał również jest równy zeru.

```{python}
import numpy as np
import matplotlib.pyplot as plt

# 1. Define the discrete time vector 'n' (e.g., from -2 to 10)
n = np.arange(-2, 11)

# 2. Initialize the signal array 'x' with zeros
x = np.zeros_len(n)

# 3. Translate the math into logic:
# The delta function only "fires" when n = 3k (which means n >= 0 and n is a multiple of 3)
# So, we find all indices where n >= 0 AND n % 3 == 0
valid_indices = (n >= 0) & (n % 3 == 0)

# For those valid points, k = n / 3. The amplitude is (-1)^k
k = n[valid_indices] // 3
x[valid_indices] = (-1.0) ** k

# 4. Plot the discrete signal using plt.stem()
# basefmt="black" makes the horizontal axis line black
plt.stem(n, x, basefmt="black", use_line_collection=True)

# Formatting the plot to make it look like a proper textbook sketch
plt.title(r"Discrete Signal $x(n) = \sum (-1)^k \delta(n-3k)$")
plt.xlabel("n (discrete time)")
plt.ylabel("x(n)")
plt.xticks(n)  # Force ticks at every integer
plt.grid(True, linestyle='--', alpha=0.7)

# Show the plot
plt.show()
```

## b.

Zanim przejdziemy do punktu B, mała, ale bardzo ważna uwaga programistyczna do kodu, który wkleiłeś.

W bibliotece NumPy nie można użyć standardowej instrukcji `if (n >= 0):`, gdy `n` jest całą tablicą (wektorem). Python wyrzuci błąd: `ValueError: The truth value of an array with more than one element is ambiguous`. Dzieje się tak, ponieważ Python nie wie, czy ma wykonać `if` dla sytuacji, gdy *wszystkie* elementy są $\ge 0$, czy *jakikolwiek* z nich. W NumPy zamiast tradycyjnego `if/else` stosujemy tzw. maskowanie logiczne (boolean indexing), dokładnie tak, jak napisałem Ci w poprzednim przykładzie: `mask = n >= 0`.

Przejdźmy teraz do Twojego drugiego zadania. Pokażę Ci, jak to rozbroić matematycznie, a na koniec napiszemy to poprawnie w Pythonie!

---

### Rozwiązanie podpunktu b: $x(n)=(-1)^{n}u(-n-4)$

Podobnie jak poprzednio, rozłóżmy ten wzór na dwa czynniki:

**1. Funkcja skoku jednostkowego $u(-n-4)$**
Standardowy skok Heaviside'a $u(n)$ działa jak włącznik: daje **1**, gdy jego argument jest większy lub równy zeru, i **0**, gdy jest mniejszy od zera.
Tutaj naszym argumentem jest wyrażenie $(-n-4)$. Zobaczmy, dla jakich wartości $n$ ta funkcja "się włączy" (czyli przyjmie wartość 1):
$$-n - 4 \ge 0$$
$$-n \ge 4$$
$$n \le -4$$
To oznacza, że nasza funkcja $u(-n-4)$ "żyje" (ma wartość 1) **tylko dla próbki $n=-4$ i wszystkich próbek mniejszych (w lewo od osi)**: $-5, -6, -7$ itd. Dla $n = -3, -2, -1, 0$ i większych, funkcja wynosi 0.

**2. Czynnik zmiennego znaku $(-1)^n$**
Ten element po prostu podnosi $-1$ do potęgi $n$. Dla parzystych wartości $n$ da 1, a dla nieparzystych da -1. Zauważ, że zasada ta działa tak samo dla liczb ujemnych: $(-1)^{-4} = 1$, a $(-1)^{-5} = -1$.

**3. Składamy sygnał w całość**
Obliczmy kilka wartości:
* Dla $n = -3$: $x(-3) = (-1)^{-3} \cdot u(-3+4) = -1 \cdot 0 = \mathbf{0}$
* Dla $n = -4$: $x(-4) = (-1)^{-4} \cdot u(4-4) = 1 \cdot 1 = \mathbf{1}$
* Dla $n = -5$: $x(-5) = (-1)^{-5} \cdot u(5-4) = -1 \cdot 1 = \mathbf{-1}$
* Dla $n = -6$: $x(-6) = (-1)^{-6} \cdot u(6-4) = 1 \cdot 1 = \mathbf{1}$
* Dla $n = -7$: $x(-7) = (-1)^{-7} \cdot u(7-4) = -1 \cdot 1 = \mathbf{-1}$

### Jak to naszkicować na papierze:
1.  **Osie:** Narysuj oś $n$ od np. $-9$ do $2$. Oś $x(n)$ z wartościami 1 i -1.
2.  **Prawa strona (zera):** Dla wszystkich punktów od $n=-3$ w prawo (czyli $-3, -2, -1, 0, 1, 2$) postaw wyraźne kropki bezpośrednio na osi poziomej (wysokość 0).
3.  **Lewa strona (prążki):** * W $n=-4$ narysuj prążek do góry na wysokość 1 i zakończ go kropką.
    * W $n=-5$ narysuj prążek w dół na wysokość -1 i zakończ kropką.
    * W $n=-6$ narysuj prążek do góry (1).
    * W $n=-7$ narysuj prążek w dół (-1).
4.  **Wielokropek:** Ponieważ sygnał ciągnie się do minus nieskończoności, po lewej stronie wykresu (np. za punktem $-8$ lub $-9$) narysuj wielokropek `...` na wysokości osi poziomej, aby pokazać, że sygnał trwa dalej w tę stronę.

---

### Kod w Pythonie (NumPy + Matplotlib)

Oto jak poprawnie wygenerować ten wykres, omijając błędy z instrukcjami `if`:

```python
import numpy as np
import matplotlib.pyplot as plt

# 1. Definiujemy wektor n (np. od -10 do 3, żeby dobrze było widać zjawisko)
n = np.arange(-10, 4)

# 2. Inicjalizujemy tablicę sygnału samymi zerami (float, żeby obsłużyć -1.0 i 1.0)
x = np.zeros_like(n, dtype=float)

# 3. MASKOWANIE LOGICZNE (Poprawny sposób w NumPy zamiast 'if')
# Znajdujemy indeksy, dla których n <= -4 (czyli tam, gdzie u(-n-4) wynosi 1)
valid_indices = n <= -4

# 4. Obliczamy wartości TYLKO dla tych miejsc, w których funkcja "żyje"
x[valid_indices] = (-1.0) ** n[valid_indices]

# 5. Rysowanie wykresu
plt.figure(figsize=(8, 4))
plt.stem(n, x, basefmt="black")

plt.title(r"Sygnał dyskretny $x(n) = (-1)^n u(-n-4)$")
plt.xlabel("n (czas dyskretny)")
plt.ylabel("x(n)")
plt.xticks(n)
plt.grid(True, linestyle='--', alpha=0.7)

# Zapis i wyświetlenie
plt.savefig("plot_b.png")
plt.show()
```
## b.

Zanim przejdziemy do punktu B, mała, ale bardzo ważna uwaga programistyczna do kodu, który wkleiłeś.

W bibliotece NumPy nie można użyć standardowej instrukcji if (n >= 0):, gdy n jest całą tablicą (wektorem). Python wyrzuci błąd: ValueError: The truth value of an array with more than one element is ambiguous. Dzieje się tak, ponieważ Python nie wie, czy ma wykonać if dla sytuacji, gdy wszystkie elementy są ≥0, czy jakikolwiek z nich. W NumPy zamiast tradycyjnego if/else stosujemy tzw. maskowanie logiczne (boolean indexing), dokładnie tak, jak napisałem Ci w poprzednim przykładzie: mask = n >= 0.

Przejdźmy teraz do Twojego drugiego zadania. Pokażę Ci, jak to rozbroić matematycznie, a na koniec napiszemy to poprawnie w Pythonie!
Rozwiązanie podpunktu b: x(n)=(−1)nu(−n−4)

Podobnie jak poprzednio, rozłóżmy ten wzór na dwa czynniki:

1. Funkcja skoku jednostkowego u(−n−4)
Standardowy skok Heaviside'a u(n) działa jak włącznik: daje 1, gdy jego argument jest większy lub równy zeru, i 0, gdy jest mniejszy od zera.
Tutaj naszym argumentem jest wyrażenie (−n−4). Zobaczmy, dla jakich wartości n ta funkcja "się włączy" (czyli przyjmie wartość 1):
−n−4≥0
−n≥4
n≤−4

To oznacza, że nasza funkcja u(−n−4) "żyje" (ma wartość 1) tylko dla próbki n=−4 i wszystkich próbek mniejszych (w lewo od osi): −5,−6,−7 itd. Dla n=−3,−2,−1,0 i większych, funkcja wynosi 0.

2. Czynnik zmiennego znaku (−1)n
Ten element po prostu podnosi −1 do potęgi n. Dla parzystych wartości n da 1, a dla nieparzystych da -1. Zauważ, że zasada ta działa tak samo dla liczb ujemnych: (−1)−4=1, a (−1)−5=−1.

3. Składamy sygnał w całość
Obliczmy kilka wartości:

    Dla n=−3: x(−3)=(−1)−3⋅u(−3+4)=−1⋅0=0

    Dla n=−4: x(−4)=(−1)−4⋅u(4−4)=1⋅1=1

    Dla n=−5: x(−5)=(−1)−5⋅u(5−4)=−1⋅1=−1

    Dla n=−6: x(−6)=(−1)−6⋅u(6−4)=1⋅1=1

    Dla n=−7: x(−7)=(−1)−7⋅u(7−4)=−1⋅1=−1

Jak to naszkicować na papierze:

    Osie: Narysuj oś n od np. −9 do 2. Oś x(n) z wartościami 1 i -1.

    Prawa strona (zera): Dla wszystkich punktów od n=−3 w prawo (czyli −3,−2,−1,0,1,2) postaw wyraźne kropki bezpośrednio na osi poziomej (wysokość 0).

    Lewa strona (prążki): * W n=−4 narysuj prążek do góry na wysokość 1 i zakończ go kropką.

        W n=−5 narysuj prążek w dół na wysokość -1 i zakończ kropką.

        W n=−6 narysuj prążek do góry (1).

        W n=−7 narysuj prążek w dół (-1).

    Wielokropek: Ponieważ sygnał ciągnie się do minus nieskończoności, po lewej stronie wykresu (np. za punktem −8 lub −9) narysuj wielokropek ... na wysokości osi poziomej, aby pokazać, że sygnał trwa dalej w tę stronę.


```{python}
import numpy as np
import matplotlib.pyplot as plt

# 1. Definiujemy wektor n (np. od -10 do 3, żeby dobrze było widać zjawisko)
n = np.arange(-10, 4)

# 2. Inicjalizujemy tablicę sygnału samymi zerami (float, żeby obsłużyć -1.0 i 1.0)
x = np.zeros_like(n, dtype=float)

# 3. MASKOWANIE LOGICZNE (Poprawny sposób w NumPy zamiast 'if')
# Znajdujemy indeksy, dla których n <= -4 (czyli tam, gdzie u(-n-4) wynosi 1)
valid_indices = n <= -4

# 4. Obliczamy wartości TYLKO dla tych miejsc, w których funkcja "żyje"
x[valid_indices] = (-1.0) ** n[valid_indices]

# 5. Rysowanie wykresu
plt.figure(figsize=(8, 4))
plt.stem(n, x, basefmt="black")

plt.title(r"Sygnał dyskretny $x(n) = (-1)^n u(-n-4)$")
plt.xlabel("n (czas dyskretny)")
plt.ylabel("x(n)")
plt.xticks(n)
plt.grid(True, linestyle='--', alpha=0.7)

# Zapis i wyświetlenie
plt.savefig("plot_b.png")
plt.show()
```

## c.

### 1. Haczyk matematyczny (Dlaczego ten sygnał to... zero?)

Rozłóżmy na czynniki funkcje skoku Heaviside'a z Twojego wzoru:
* **$u(n+3)$**: Ta funkcja przyjmuje wartość $1$, gdy $n+3 \ge 0$, czyli dla **$n \ge -3$**. (Są to wartości: $-3, -2, -1, 0...$)
* **$u(-n-5)$**: Ta funkcja przyjmuje wartość $1$, gdy $-n-5 \ge 0$, co daje $-n \ge 5$, czyli **$n \le -5$**. (Są to wartości: $-5, -6, -7...$)

Twój sygnał to iloczyn tych dwóch warunków. Aby sygnał był różny od zera, **oba te warunki muszą być spełnione jednocześnie**.
Zadajmy sobie pytanie: *Czy istnieje liczba całkowita $n$, która jest jednocześnie większa lub równa $-3$ ORAZ mniejsza lub równa $-5$?*

**Nie ma takiej liczby.** Zbiór części wspólnej jest pusty. Oznacza to, że iloczyn $u(n+3)u(-n-5)$ zawsze wynosi zero. Cokolwiek pomnożysz przez zero (nawet Twojego cosinusa), da zero.

Szkic tego sygnału to po prostu **płaska linia zer (kropki na osi poziomej)** dla każdego możliwego $n$. Jeśli to zadanie z listy, to najpewniej wykładowca sprawdza, czy bezmyślnie podstawiacie do wzoru, czy analizujecie dziedzinę! *(Chyba że prowadzący pomylił się w znakach tworząc zadanie – gdyby to było np. $u(n+5)u(3-n)$, to powstałoby tzw. "okno" od $-5$ do $3$).*

---

### 2. Poprawki w Twoim kodzie Python

Nawet jeśli sygnał wynosi zero, warto wiedzieć, dlaczego Twój kod rzuciłby błędem. Oto 3 złote zasady NumPy, które u Ciebie zawiodły:

1.  **Nawiasy przy operatorach bitowych:** W Pythonie operator `&` ma wyższy priorytet niż operatory porównania (`<=`, `>=`). Jeśli napiszesz `n <= -5 & n >= -3`, Python najpierw spróbuje obliczyć `-5 & n`, co wyrzuci błąd. **Zawsze używaj nawiasów:** `(n <= -5) & (n >= -3)`.
2.  **Indeksowanie każdej zmiennej `n`:** Kiedy używasz maski `valid_indices` po lewej stronie znaku równości, musisz jej użyć wszędzie po prawej stronie, gdzie występuje `n`. Zamiast `np.cos(np.pi/2*n)`, musi być `np.cos(np.pi/2*n[valid_indices])`.
3.  **Nadmiarowe mnożenie:** W kodzie napisałeś `... * n[valid_indices]`. We wzorze matematycznym nie masz mnożenia cosinusa przez $n$ (jest tylko argument cosinusa).

### Poprawiony kod dla podpunktu C

Oto kod, który wykonuje się bezbłędnie i udowadnia matematyczny fakt, że ten sygnał to same zera (zmieniłem też tytuł wykresu na poprawny):

```python
import numpy as np
import matplotlib.pyplot as plt

n = np.arange(-10, 10)
x = np.zeros_like(n, dtype=float)

# Poprawiony warunek logiczny z nawiasami
valid_indices = (n <= -5) & (n >= -3)

# Poprawione indeksowanie (choć maska jest pusta, to tak wygląda poprawny zapis)
x[valid_indices] = np.cos(np.pi / 2 * n[valid_indices])

plt.figure(figsize=(8, 4))
plt.stem(n, x, basefmt="black")

# Zaktualizowany tytuł (korzystamy z surowego stringa 'r' dla LaTeXa)
plt.title(r"Discrete signal $x(n) = \cos(\frac{\pi}{2}n) u(n+3) u(-n-5)$")
plt.xlabel("n (discrete time)")
plt.ylabel("x(n)")
plt.xticks(n)
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig("plot_c.png")
plt.show()
```

# 2.2

Wyznaczenie odpowiedzi impulsowej na podstawie takiego równania różnicowego to jedno z najprzyjemniejszych i najszybszych zadań w cyfrowym przetwarzaniu sygnałów. Nie wymaga ono skomplikowanych matematycznych przekształceń (jak np. transformata Z), a jedynie sprowadza się do zastosowania podstawowej definicji.

Oto jak należy to rozwiązać krok po kroku:

### 1. Definicja odpowiedzi impulsowej $h(n)$
Odpowiedź impulsowa to, najprościej mówiąc, sygnał, jaki pojawi się na wyjściu systemu (czyli $y(n)$), gdy na jego wejście podamy **pojedynczy impuls**, czyli dyskretną funkcję delta-Diraca (Kroneckera):
$$x(n) = \delta(n)$$

### 2. Podstawienie do równania
Skoro wiemy, że $h(n)$ to po prostu $y(n)$ w reakcji na impuls $\delta(n)$, wystarczy w Twoim równaniu systemowym podmienić symbole:
* Sygnał wyjściowy $y(n)$ zamieniamy na odpowiedź impulsową $h(n)$.
* Każde wystąpienie sygnału wejściowego $x(n)$ zamieniamy na $\delta(n)$, zachowując oryginalne przesunięcia w czasie (opóźnienia).

Twój system wejściowy to:
$$y(n) = x(n-5) + \frac{1}{2}x(n-7)$$

Dokonując podstawienia, otrzymujemy ostateczny wynik:
**$$h(n) = \delta(n-5) + \frac{1}{2}\delta(n-7)$$**

# 2.3
To zadanie jest świetnym sprawdzianem tego, jak dobrze rozumiesz równania różnicowe. Nie musimy tu zgadywać wzoru sygnału wejściowego $x(n)$ – wystarczy, że odczytamy jego wartości z wykresu, a następnie wstawimy do podanego równania krok po kroku.

*(Mała uwaga na marginesie: W treści zadania napisano, że system jest LTI, czyli stacjonarny/niezmienny w czasie. W rzeczywistości człon $(-1)^n$ sprawia, że system jest **zmienny w czasie**. Prawdopodobnie to małe niedopatrzenie autora zadania, ale nie przeszkadza nam to w niczym, by po prostu policzyć $y(n)$ ze wzoru!)*

Rozwiążmy to razem.

### 1. Odczytanie sygnału $x(n)$ z wykresu

Z obrazka, który załączyłeś, możemy spisać wszystkie niezerowe wartości sygnału wejściowego:
* $x(0) = 1$
* $x(1) = 2$
* $x(2) = 3$
* $x(3) = 1$

Dla wszystkich pozostałych wartości $n$ (np. ujemnych oraz od $4$ w górę) sygnał $x(n) = 0$.

### 2. Obliczenia krok po kroku

Nasz system opisany jest równaniem:
$$y(n) = (-1)^{n}x(n) + 2x(n-1)$$

Musimy sprawdzić po kolei każdą próbkę. Ponieważ sygnał $x(n)$ pojawia się w $n=0$, a człon $2x(n-1)$ wprowadza opóźnienie o jedną próbkę, sygnał wyjściowy $y(n)$ będzie miał wartości niezerowe od $n=0$ aż do $n=4$. Obliczmy je:

* **Dla $n = -1$:** (Sprawdzamy na wszelki wypadek)
    $y(-1) = (-1)^{-1}x(-1) + 2x(-2) = -1 \cdot 0 + 2 \cdot 0 = \mathbf{0}$

* **Dla $n = 0$:**
    $y(0) = (-1)^{0}x(0) + 2x(-1) = 1 \cdot 1 + 2 \cdot 0 = \mathbf{1}$

* **Dla $n = 1$:**
    $y(1) = (-1)^{1}x(1) + 2x(0) = -1 \cdot 2 + 2 \cdot 1 = -2 + 2 = \mathbf{0}$

* **Dla $n = 2$:**
    $y(2) = (-1)^{2}x(2) + 2x(1) = 1 \cdot 3 + 2 \cdot 2 = 3 + 4 = \mathbf{7}$

* **Dla $n = 3$:**
    $y(3) = (-1)^{3}x(3) + 2x(2) = -1 \cdot 1 + 2 \cdot 3 = -1 + 6 = \mathbf{5}$

* **Dla $n = 4$:** (Sygnał wejściowy $x(4)$ to już zero, ale jest jeszcze "ogon" z opóźnienia)
    $y(4) = (-1)^{4}x(4) + 2x(3) = 1 \cdot 0 + 2 \cdot 1 = 0 + 2 = \mathbf{2}$

* **Dla $n = 5$:**
    $y(5) = (-1)^{5}x(5) + 2x(4) = -1 \cdot 0 + 2 \cdot 0 = \mathbf{0}$

### 3. Jak naszkicować to na papierze

Szkic wykonaj dokładnie tak, jak wyglądał sygnał wejściowy z zadania, ale nanieś nowe punkty:
1.  **Oś pozioma ($n$):** Zaznacz zakres od np. $-2$ do $6$.
2.  **Oś pionowa ($y(n)$):** Musi teraz sięgać wyżej, aż do wartości $7$.
3.  **Prążki:**
    * W $n=0$ narysuj pionową linię (prążek) do wartości **$1$**.
    * W $n=1$ postaw kropkę na samej osi (wartość **$0$**). To bardzo ważny punkt wykresu, bo pokazuje znoszenie się sygnałów!
    * W $n=2$ narysuj długi prążek do wartości **$7$**.
    * W $n=3$ narysuj prążek do wartości **$5$**.
    * W $n=4$ narysuj prążek do wartości **$2$**.
4.  **Zera:** Pamiętaj, aby postawić kropki bezpośrednio na osi poziomej dla $n = -2, -1$ oraz $n = 5, 6, 7$, aby zaznaczyć, że sygnał wynosi tam $0$.

---

### Kod w Pythonie (żebyś mógł to sam wygenerować!)

Ponieważ widzę, że bardzo dobrze radzisz sobie z NumPy i Matplotlib, przygotowałem dla Ciebie gotowy kod na ten wykres. Zauważ, jak łatwo implementuje się to w kodzie przy pomocy metody przesunięcia tablicy.

```python
import numpy as np
import matplotlib.pyplot as plt

# Wektor czasu n
n = np.arange(-2, 8)

# Ręcznie wprowadzamy wartości sygnału x(n) odczytane z wykresu
# Indeksy:   -2, -1, 0, 1, 2, 3, 4, 5, 6, 7
x = np.array([0,  0, 1, 2, 3, 1, 0, 0, 0, 0])

# Obliczamy x(n-1) po prostu przesuwając wektor x o jedno miejsce w prawo
# Używamy np.roll i zerujemy pierwszy element, żeby symulować wejście zer z lewej strony
x_delayed = np.roll(x, 1)
x_delayed[0] = 0

# Obliczamy sygnał y(n) ze wzoru matematycznego
y = ((-1.0)**n) * x + 2 * x_delayed

# Rysowanie
plt.figure(figsize=(8, 4))
plt.stem(n, y, basefmt="black")

plt.title(r"Sygnał wyjściowy $y(n) = (-1)^n x(n) + 2x(n-1)$")
plt.xlabel("n (czas dyskretny)")
plt.ylabel("y(n)")
plt.xticks(n)
plt.yticks(np.arange(0, 9, 1)) # Wymuszamy podziałkę co 1 na osi Y
plt.grid(True, linestyle='--', alpha=0.7)

plt.show()
```

# 2.5

Świetna obserwacja! Bardzo dobrze odczytałeś ten wykres. Zauważenie, że sygnał jest okresowy, a jego okres wynosi $T = 2\pi$ (nawet jeśli na osi niefortunnie wydrukowano "n" zamiast "$\pi$"), to klucz do sukcesu w tym zadaniu.

Na wstępie mała uwaga: w treści zadania, którą wkleiłeś, jest literówka – napisano $x(1)$, ale z wykresu i kontekstu jasno wynika, że chodzi o ciągły sygnał w dziedzinie czasu, czyli **$x(t)$**.

Rozprawmy się z energią i mocą tego sygnału krok po kroku.

### 1. Definicja sygnału w jednym okresie
Aby cokolwiek policzyć, musimy opisać ten sygnał wzorem matematycznym na przedziale jednego okresu, czyli dla $t \in [0, 2\pi]$:
* W przedziale od $0$ do $\pi$ sygnał to po prostu "górna" połówka sinusoidy o amplitudzie 1: **$x(t) = \sin(t)$**
* W przedziale od $\pi$ do $2\pi$ sygnał jest stały i wynosi: **$x(t) = -0.5$**

### 2. Energia sygnału ($E$)
Z definicji, energia całkowita sygnału to pole podniesionej do kwadratu funkcji na przedziale od $-\infty$ do $\infty$.

Twój sygnał jest okresowy (powtarza się w nieskończoność w lewo i w prawo). Z każdym kolejnym okresem dostarcza kolejną "porcję" energii. Jeśli będziemy dodawać te porcje w nieskończoność, wynik również urośnie do nieskończoności.

Złota zasada teorii sygnałów mówi: **Każdy sygnał okresowy o niezerowej amplitudzie ma nieskończoną energię.**
Zatem pierwsza część odpowiedzi to po prostu:
$$E = \infty$$

### 3. Moc sygnału ($P$)
Skoro energia jest nieskończona, do opisu takich sygnałów używamy **mocy średniej**. Moc mówi nam o tym, ile energii sygnał niesie średnio w czasie jednego okresu $T$.

Wzór na moc sygnału okresowego to:
$$P = \frac{1}{T} \int_{0}^{T} |x(t)|^2 dt$$

Podstawmy nasze dane ($T = 2\pi$) i rozbijmy całkę na dwa przedziały, tak jak zdefiniowaliśmy sygnał:
$$P = \frac{1}{2\pi} \left[ \int_{0}^{\pi} (\sin(t))^2 dt + \int_{\pi}^{2\pi} (-0.5)^2 dt \right]$$

Teraz wystarczy rozwiązać te dwie całki osobno:

**Całka 1 (część sinusoidalna):**
Do scałkowania $\sin^2(t)$ najlepiej użyć wzoru trygonometrycznego na kąt podwojony: $\sin^2(t) = \frac{1 - \cos(2t)}{2}$.
$$\int_{0}^{\pi} \sin^2(t) dt = \int_{0}^{\pi} \left( \frac{1}{2} - \frac{\cos(2t)}{2} \right) dt = \left[ \frac{t}{2} - \frac{\sin(2t)}{4} \right]_{0}^{\pi}$$
Podstawiamy granice całkowania: $\left( \frac{\pi}{2} - 0 \right) - (0 - 0) = \mathbf{\frac{\pi}{2}}$

**Całka 2 (część stała):**
$$\int_{\pi}^{2\pi} (-0.5)^2 dt = \int_{\pi}^{2\pi} 0.25 dt = 0.25 \cdot t \Big|_{\pi}^{2\pi} = 0.25 \cdot (2\pi - \pi) = 0.25\pi = \mathbf{\frac{\pi}{4}}$$

**Złożenie w całość:**
Teraz wstawiamy wyniki obu całek do głównego wzoru na moc:
$$P = \frac{1}{2\pi} \left( \frac{\pi}{2} + \frac{\pi}{4} \right)$$
$$P = \frac{1}{2\pi} \left( \frac{2\pi}{4} + \frac{\pi}{4} \right)$$
$$P = \frac{1}{2\pi} \left( \frac{3\pi}{4} \right)$$
Skracamy $\pi$:
$$P = \frac{3}{8}$$


