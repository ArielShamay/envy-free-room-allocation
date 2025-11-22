הנה הצעה ל-**README.md** איכותי ומקצועי בעברית, שכתוב בצורה שמתאימה להגשה או לתיעוד ב-GitHub. הוא משלב את ההסברים התיאורטיים מהמקורות שלך, את הלוגיקה האלגוריתמית, ואת הניתוח של תוצאות הבדיקות הספציפיות שעשית.

-----

# אלגוריתם חלוקת חדרים ללא קנאה (Envy-Free Room Allocation)

פרויקט זה מממש פתרון אלגוריתמי לבעיית "חלוקת שכר דירה" (Rent Division). המטרה היא להקצות חדרים לשותפים ולקבוע את המחיר שכל שותף ישלם, כך שסכום התשלומים יכסה בדיוק את שכר הדירה הכולל, והחלוקה תהיה **ללא קנאה** (Envy-Free).

## 📌 הגדרת הבעיה

נתונה דירה עם $n$ חדרים ו-$n$ שותפים, וסכום שכירות כולל $R$. לכל שותף יש הערכה כספית (Valuation) סובייקטיבית לכל חדר. אנו מניחים שהשותפים הם **קוואזיליניאריים** (Quasilinear), כלומר התועלת של שותף $i$ מחדר $j$ במחיר $p_j$ היא:
$$Utility_{i} = Value_{i}(Room_{j}) - p_{j}$$

**האתגר:** למצוא השמה $X$ (מי מקבל איזה חדר) ווקטור מחירים $p$ כך ש:

1.  $\sum p_j = R$ (המחירים מכסים את השכירות).
2.  [cite\_start]אף שותף לא מעדיף את החבילה (חדר + מחיר) של שותף אחר [cite: 729-730].

## 💡 הפתרון האלגוריתמי

[cite\_start]הפתרון מבוסס על המשפט הקובע כי השמה הממקסמת את סכום הערכים (Social Welfare) היא תנאי הכרחי ומספיק לקיום תמחור ללא קנאה[cite: 938]. האלגוריתם פועל בשני שלבים:

### שלב א': השמה (Assignment)

מציאת השמה שממקסמת את סכום הערכים של כל השחקנים יחד.

  * **המימוש:** הבעיה ממומלת כבעיית שידוך בגרף דו-צדדי ממושקל (Bipartite Matching).
  * [cite\_start]**טכנולוגיה:** שימוש ב-`scipy.optimize.linear_sum_assignment` (או המקביל ל"אלגוריתם ההונגרי") למציאת **Maximum Weight Perfect Matching**[cite: 963, 998].

### שלב ב': תמחור (Pricing)

חישוב המחירים כך שאף שחקן לא יקנא.

  * [cite\_start]**גרף הקנאה:** בניית גרף מכוון בו כל צומת הוא שחקן, ומשקל הקשת $i \to j$ הוא רמת הקנאה של $i$ ב-$j$ תחת ההשמה הנוכחית [cite: 881-882].
  * **חישוב סובסידיות:** מכיוון שההשמה אופטימלית, מובטח שבגרף אין מעגלים חיוביים. [cite\_start]אנו מחשבים את **המסלול הכבד ביותר** (Longest Path) מכל צומת, המסומן ב-$q_i$ (סובסידיה) [cite: 917-918]. החישוב מתבצע באמצעות אלגוריתם **Bellman-Ford** (על משקלים שליליים).
  * [cite\_start]**קביעת המחיר הסופי:** המחיר לכל חדר נקבע על ידי חלוקת ה"גירעון" שנוצר מהסובסידיות שווה בשווה בין כל השחקנים, כך שסכום המחירים הסופי יהיה $R$[cite: 932].

## 🧪 בדיקות ותוצאות (Testing & Verification)

הקוד נבדק על מקרי קצה ומקרים סטנדרטיים כדי לוודא נכונות מתמטית. להלן ניתוח התוצאות:

### 1\. מקרה "הטרמפיסט" (The Free-Rider Problem)

במקרה זה נבדקה סיטואציה קיצונית בה שחקן אחד מעריך את החדרים בסכום גבוה משמעותית מהשני, והשני מעריך אותם בערך נמוך מאוד (קרוב ל-0).

  * **קלט:** `valuations = [[150, 0], [140, 10]]`, `rent = 100`.
  * **תוצאה שהתקבלה:** השחקן השני משלם מחיר **שלילי** (מקבל כסף, כ-15-), בעוד השחקן הראשון משלם יותר מסך השכירות (115).
  * [cite\_start]**ניתוח:** תוצאה זו תואמת בדיוק את התיאוריה [cite: 1021-1028]. כדי למנוע מהשחקן השני לקנא בשחקן הראשון (שקיבל את החדר הטוב), ההפרש במחירים חייב להיות גדול, מה שמחייב תשלום שלילי ("סבסוד") לשחקן שקיבל את החדר הגרוע. זהו אימות קריטי לכך שהאלגוריתם לא "מפחד" ממחירים שליליים ומטפל נכון באילוצי קנאה קשיחים.

### 2\. המקרה הסטנדרטי (Standard Example)

נבדקה דוגמה קלאסית עם 3 שותפים ו-3 חדרים בעלי ערכים מגוונים.

  * **קלט:** `valuations` לפי הטבלה בכיתה, `rent = 100`.
  * **תוצאה שהתקבלה:**
      * Player 0: משלם \~33.33
      * Player 1: משלם \~43.33
      * Player 2: משלם \~23.33
  * **ניתוח:** סכום המחירים הוא בדיוק 100. בדיקה ידנית מאשרת שעבור כל שחקן, הערך פחות המחיר (התועלת) גבוה או שווה לתועלת שהיה מקבל מכל חדר אחר. [cite\_start]תוצאה זו זהה לפתרון האגליטרי המופיע במקורות[cite: 332], מה שמעיד על דיוק החישוב של המסלולים הכבדים בגרף.

## 🚀 איך להריץ

הפרויקט כתוב ב-Python ודורש את הספריות `numpy`, `scipy` (אופציונלי לשידוך), ו-`networkx` (לניהול הגרף).

```bash
python envy_free_allocation.py
```

הפלט יציג את ההשמה הנבחרת ואת המחיר המחושב לכל חדר, יחד עם אימות (Assertion) שהפתרון הוא אכן Envy-Free.
