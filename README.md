לגוריתם חלוקת חדרים ללא קנאה (Envy-Free Room Allocation)פרויקט זה מממש פתרון אלגוריתמי לבעיית "חלוקת שכר דירה" (Rent Division). המטרה היא להקצות חדרים לשותפים ולקבוע את המחיר שכל שותף ישלם, כך שסכום התשלומים יכסה בדיוק את שכר הדירה הכולל, והחלוקה תהיה ללא קנאה (Envy-Free).📌 הגדרת הבעיהנתונה דירה עם $n$ חדרים ו-$n$ שותפים, וסכום שכירות כולל $R$. לכל שותף יש הערכה כספית (Valuation) סובייקטיבית לכל חדר.אנו מניחים שהשותפים הם קוואזיליניאריים (Quasilinear), כלומר התועלת של שותף $i$ מחדר $j$ במחיר $p_j$ היא הערך שהוא מייחס לחדר פחות המחיר שעליו לשלם:$$Utility_i = Value_i(Room_j) - p_j$$האתגר: למצוא השמה $X$ (מי מקבל איזה חדר) ווקטור מחירים $p$ כך שיתקיימו שני תנאים:סכום המחירים שווה לשכר הדירה הכולל ($R$).ללא קנאה: אף שותף לא מעדיף את החבילה (חדר + מחיר) שקיבל שותף אחר1.💻 ממשק הקוד (Required Interface)בהתאם לדרישות המטלה, המימוש מתבצע בפייתון והפונקציה המרכזית נכתבה לפי החתימה הבאה 2:Pythondef envy_free_room_allocation(valuations: list[list[float]], rent: float) -> tuple[dict, dict]:
    """
    Calculates an envy-free allocation of rooms and prices.
    Input:
        valuations: Matrix where row i is player i's value for each room.
        rent: Total rent sum.
    Output:
        Returns assignment and pricing dictionaries.
    """
    # Implementation...
💡 הפתרון האלגוריתמיהפתרון מבוסס על המשפט הקובע כי השמה הממקסמת את סכום הערכים (Social Welfare) היא תנאי הכרחי ומספיק לקיום תמחור ללא קנאה 3. האלגוריתם פועל בשני שלבים:שלב א': השמה (Assignment)מציאת השמה שממקסמת את סכום הערכים של כל השחקנים יחד.המימוש: הבעיה ממומלת כבעיית שידוך בגרף דו-צדדי ממושקל (Maximum Weight Perfect Matching) 4.טכנולוגיה: שימוש בפונקציה linear_sum_assignment (מתוך ספריית scipy) או באלגוריתם דומה למציאת שידוך אופטימלי.שלב ב': תמחור (Pricing)חישוב המחירים כך שאף שחקן לא יקנא.גרף הקנאה: בניית גרף מכוון בו כל צומת הוא שחקן, ומשקל הקשת מ-$i$ ל-$j$ הוא רמת הקנאה של $i$ ב-$j$ תחת ההשמה הנוכחית 5.חישוב סובסידיות: מכיוון שההשמה אופטימלית, מובטח שבגרף אין מעגלים חיוביים6. אנו מחשבים את המסלול הכבד ביותר (Longest Path) מכל צומת באמצעות אלגוריתם Bellman-Ford (או וריאציה המתאימה למשקלים בגרף ללא מעגלים חיוביים) 7.קביעת המחיר הסופי: ערך המסלול הכבד ביותר מגדיר את ה"סובסידיה" לכל שחקן. המחיר הסופי נקבע על ידי קיזוז הגירעון שנוצר מהסובסידיות שווה בשווה בין כל השחקנים8888.🧪 בדיקות ותוצאות (Testing & Verification)הקוד נבדק על מקרי קצה ומקרים סטנדרטיים כדי לוודא נכונות מתמטית. להלן ניתוח התוצאות:1. מקרה "הטרמפיסט" (The Free-Rider Problem)במקרה זה נבדקה סיטואציה קיצונית בה שחקן אחד מעריך את החדרים בסכום גבוה משמעותית מהשני.הקלט: valuations = [[150, 0], [140, 10]], rent = 100.התוצאה שהתקבלה: השחקן השני משלם מחיר שלילי (כלומר, מקבל כסף, כ-15-), בעוד השחקן הראשון משלם יותר מסך השכירות (115).ניתוח: תוצאה זו תואמת בדיוק את התיאוריה 9. כדי למנוע קנאה, השחקן שקיבל את החדר הפחות רצוי חייב לקבל פיצוי משמעותי ("סבסוד"), מה שמוביל למחיר שלילי.2. המקרה הסטנדרטינבדקה דוגמה קלאסית עם 3 שותפים ו-3 חדרים.התוצאה שהתקבלה: המחירים חושבו כ-33.33, 43.33 ו-23.33 (בקירוב).ניתוח: סכום המחירים הוא בדיוק 100. בדיקה הראתה שעבור כל שחקן מתקיים תנאי האי-קנאה. תוצאה זו זהה לפתרון האגליטרי המופיע במקורות10, מה שמעיד על דיוק החישוב.🚀 הרצההפרויקט דורש את הספריות numpy ו-scipy (לחישוב השידוך).ניתן להריץ את הקובץ הראשי כדי לראות את הפלט של הדוגמאות:Bashpython envy_free_allocation.py
