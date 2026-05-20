دليل المستخدم - مكتبة CWidgets V0.1.2:

## مقدمة
CWidgets: قوتك في البرمجة بلا حدود
حول عوائق Qt إلى فرص إبداعية
CWidgets هي مكتبة بايثون متخصصة تمنح المطورين المكفوفين السيطرة الكاملة على واجهات PyQt6 وPySide6. 
لقد إنتهى زمن القيود مع QTextEdit،  فمنذ الآن، يمكنك تصميم واجهات تحتوي على مربعات تحرير متعددة الأسطر بكل حرية وتوافقية.
المكتبة توفر للمطور الكفيف توافقية مطلقة فجميع العناصر مصممة لتعمل بسلاسة تامة مع قارئ الشاشة NVDA.
إستمرارية الإبداع:لا حاجة لتعلم أدوات جديدة بل واصل كتابة أكوادك التي تعودت عليها مع الحفاظ على نفس الدوال والوظائف.
هندسة ذكية:كل عنصر في CWidgets يرث خصائص عناصر Qt الأصلية، مما يضمن لك أداءً قياسياً مع حلول جذرية لمشاكل التوافقية.
ما الذي سيتغيّر عند كتابة أكواد برامجك التي تصممها بنوافذ PyQt6 و PySide6 ؟ 
كل ما تحتاجه هو استبدال الحرف الأول فقط (C عوضاً عن Q):
CTextEdit بدلاً من QTextEdit.
CButton بدلاً من QPushButton.
حيث ترمز C إلى Custom أو مخصصة
مرونة تامة في العمل ، فالمكتبة تدعم بيئة العمل التي تفضلها بنفس الكفاءة:
مع PySide6:
from cwidgets.pyside6 import CButton, CLabel, CLineEdit

مع PyQt6:
from cwidgets.pyqt6 import CButton, CLabel, CLineEdit
CWidgets: برمج بكل ثقة، وصمم بلا قيود.

##المكونات المتوفرة :
7 عناصر مخصصة متوافقة تماما توفرها لك هذه المكتبة و هي :
1-CTextEdit 
2-CButton 
3-CLabel
4-CLineEdit 
5-CComboBox
6-CListWidget 
7-CMessageBox 

## التثبيت

    pip install cwidgets


## الوصول إلى المساعدة

بعد التثبيت، أبدأ بالتعرف على المكتبة و مكوناتها و خصائصها و كيفية إستخدامها من خلال هذه الدوال :
import cwidgets

# قائمة بجميع المكونات المتاحة
cwidgets.widgets()

# قائمة بجميع الأقسام المتاحة
cwidgets.sections()

# فتح الدليل الكامل في المتصفح
cwidgets.show_help()
cwidgets.show_help(lang="ar")

# فتح أحد المكونات بالتحديد مباشرة
cwidgets.show_help(lang="ar", goto="CButton")
cwidgets.show_help(lang="ar", goto="CTextEdit")

# فتح قسم محدد مباشرة
cwidgets.show_help(lang="ar", goto="introduction")
cwidgets.show_help(lang="ar", goto="installation")

## المشاكل الشائعة التي تم حلها

#CTextEdit : 
مربع تحرير متعدد الأسطر: يحل CTextEdit المشكلة الأساسية لـ QTextEdit، غير المتوافق مع NVDA.
#CComboBox & CListWidget: 
فصل التنقل عن التفعيل : فصل إجراءات التنقل (الأسهم) عن إجراءات التفعيل (Enter/Space) لتجنب التفعيلات غير المقصودة.
التعطيل المتاح: الحفاظ على الإعلان بواسطة NVDA حتى عندما يكون المكون معطلاً .
#CButton : 
التفعيل ب enter, return, space & mouse .
توافقية حتى في حالة التعطيل .
#CLabel 
تعزيز توافقية العناوين والملصقات
#CLineEdit : 
يمكنك من إسترجاع النص من داخل العنصر من خلال الضغط enter دون أي سطر كود إضافي .
#CMessageBox :
محاورة رسائل ذاتية الإنهيار .
يمكنك تحديد زمن تختفي بعده المحاورة تلقائيا .
#بإستثناء CTextEdit ، كل المكونات الأخرى ترث من QT و بالتالي هي تحتفظ بكل خصائصها و وظائفها الأساسية .
## تفاصيل المكونات : 
التعريف ،الإنشاء ، الخصائص ، الإستخدام .
## CTextEdit

### التعريف
CTextEdit هو مربع تحرير متعدد الأسطر متوافق تماما مع NVDA .
### لماذا — المشكلة الأساسية
- QTextEdit الأصلي في Qt غير متوافق مع NVDA.
— المطور الكفيف لا يمكنه القراءة أو الكتابة في هذا العنصر .
هذا هو الحاجز الذي يحول دون المكفوفين و تصميم واجهات QT تحتوي على مربعات تحرير متعددة الأسطر .
إلى حد ظهور هذه المكتبة لم تعرف حلولا لهذه المشكلة يستخدمها المكفوفون .

### الحل — RichEdit Win32 مدمج في Qt
الحل الذي أتت به هذه المكتبة هو دمج عنصر تحكم Win32 RichEdit مباشرة في نافذة QT .
RichEdit Win32 هو إفتراضيا متوافق تماما مع NVDA .
المرحلة المعقدة في تصميم الحل هي دمجه في نافذة Qt مع الحفاظ على إمكانية الوصول هذه.
كما ضمنت هذه المكتبة الإستخدام الإفتراضي للأوامر في QT .
بنية العنصر QTextEdit :
-QTextEdit 
-EditorStyle        — الأنماط، الخط، اللون، المحاذاة
-RichEdit Win32  — المحرك الأصلي  المتوافق 

### الميزات
- إمكانية الوصول الكاملة بواسطة NVDA: القراءة، الكتابة، التنقل، التحديد.
- واجهة برمجة تطبيقات متوافقة مع QTextEdit: setText, toPlainText, append, clear, setReadOnly.
- نص منسق: الخط، الحجم، غامق، مائل، اللون، المحاذاة.
- إدارة غير متزامنة: الأنماط والنص في الانتظار إذا لم يكن مقبض Win32 متاحًا بعد.
- التركيز الذكي: استعادة التركيز عند العودة إلى التطبيق.

### الاستخدام

    # PySide6
    from cwidgets.pyside6 import CTextEdit
    # PyQt6
    from cwidgets.pyqt6 import CTextEdit

    # إنشاء
    self.editor = CTextEdit(self, accessible_name="إسم المربع")
    layout.addWidget(self.editor)

    # إدراج نص داخل المربع
    self.editor.setText("مرحبًا!")
# إسترجاع النص من داخل المربع :
    text = self.editor.text()
    text = self.editor.toPlainText()
#إضافة نص إلى النص الأصلي 
    self.editor.append("سطر جديد.")
#مسح النص لإفراغ المربع  
    self.editor.clear()

    # جعل المربع  للقراءة فقط
    self.editor.setReadOnly(True)
#تعطيل للقراءة فقط ليصبح المربع للكتابة و القراءة 
    self.editor.setReadOnly(False)

    # الخط — QFont أو (str, int, bool, bool)
    self.editor.setFont("Arial", 12, True, False)  # الاسم، الحجم، غامق، مائل

    # الألوان — اسم أو مجموعة RGB
    self.editor.setTextColor("red")
    self.editor.setTextColor((255, 0, 0))
    self.editor.setBackgroundColor("yellow")

    # المحاذاة
    self.editor.setAlignment("left")
    self.editor.setAlignment("center")
    self.editor.setAlignment("right")

### الألوان المتاحة

    # الأسماء المدعومة
    "black", "white", "red", "green", "blue", "yellow",
    "cyan", "magenta", "gray", "darkgray", "lightgray",
    "orange", "purple", "violet", "pink", "brown",
    "navy", "teal", "lime", "olive", "maroon",
    "coral", "salmon", "gold", "silver"

    # أو مجموعة RGB
    (255, 0, 0)    # أحمر
    (0, 128, 255)  # أزرق فاتح

### العنوان المرئي اختياري
accessible_name يُقرأه  NVDA ولكنه غير مرئي بصريًا.
لإضافة عنوان مرئي، أضف CLabel إلى التخطيط قبل المحرر:
    self.editor = CTextEdit(self)
    self.lbl    = CLabel("مربع التحرير:", self , self.editor)
و هنا من الضروري التنبيه أن إضافة CLabel إلى layout يجب أن تسبق إضافة editor حتى يظهر إسم المربع فوق المربع و ليس تحته .
    layout.addWidget(self.lbl)
    layout.addWidget(self.editor)

## CLabel

### التعريف
CLabel هو ملصق متوافق مع NVDA، يحل محل QLabel.

### لماذا؟
QLabel الأصلي غير مرئي لـ NVDA إلا إذا كان مرتبطًا بـ buddy — وفقط عندما يكون هذا Buddy لديه التركيز.

### الحل
وضعان:
- الوضع الفردي: متوافق مع NVDA و يتعرف عليه حتى بالتنقل بالتاب .
- وضع Buddy: عندما يكون CLabel مرتبطا بعنصر آخر .

### الميزات
- تنظيف الاختصارات: &الاسم → "الاسم" لـ NVDA، الاختصار المرئي لـ Qt محفوظ.
- prefix نص تكميلي مثال عندما نريد التعبير عن حالة status .

- المزامنة الإفتراضية :
تغيير محتوى الملصق .
setText()
تغيير النص التكميلي :
setPrefix()
يعيدان المزامنة بدون كود إضافي.

### الاستخدام

    # PySide6
    from cwidgets.pyside6 import CLabel, CLineEdit
    # PyQt6
    from cwidgets.pyqt6 import CLabel, CLineEdit

    # الوضع الفردي — يقرأ NVDA النص و يمكن الوصول إليه بالتاب :
    self.lbl = CLabel("تم حفظ الملف", self)

    # مع prefix — يعلن NVDA: "حالة تم حفظ الملف"
    self.lbl = CLabel("تم حفظ الملف", self, prefix="حالة")

    # وضع Buddy — يعلن NVDA الملصق عندما يحصل الحقل على التركيز
    # يجب إضافة الملصق إلى التخطيط قبل حقل الكتابةحتى يظهر الملصق فوق الحقل بصريا  
    self.edit = CLineEdit(self)
    self.lbl  = CLabel("الاسم:", self, self.edit)
    layout.addWidget(self.lbl)
    layout.addWidget(self.edit)

    # التحديث الديناميكي
    self.lbl.setText("جارٍ المعالجة")
    self.lbl.setPrefix("خطأ")

## CButton

### التعريف
CButton هو زر يتميز بمزايا إضافية تجعله قابلا للإستخدام دون الحاجة لأسطر كودية يحتاج الزر الأصلي لتلك الأسطر لتفعيل هذه المزايا .

### لماذا؟
- QPushButton الأصلي يقبل فقط Space للتفعيل — Enter و Return يتم تجاهلهما.
- setEnabled(False) يجعل الزر غير مرئي لـ NVDA، حتى مع setAccessibleDescription.

### الحل
- التفعيل يشمل Enter/Return.
- تعطيل  الزر يتم مع مواصلة التوافقية .
الزر يبقى بصريا "في حالة نشطة" لكنه لا يعمل.
و هذا هو الحل:  توفر إمكانية التعطيل مع إستمرار التوافقية عكس QPushButton الذي يختفي عن NVDA لو كان معطلا .

### الميزات
- التفعيل الموسع: Space، Enter، Return، النقر بالماوس.
- التعطيل المتاح: غير قابل للنقر + يعلن NVDA "غير متاح".
- واجهة برمجة تطبيقات مطابقة لـ QPushButton.

### الاستخدام

    # PySide6
    from cwidgets.pyside6 import CButton
    # PyQt6
    from cwidgets.pyqt6 import CButton

    self.btn = CButton("حفظ", self)
    self.btn.clicked.connect(self.on_click)

    # تعطيل — يعلن NVDA "غير متاح"، الزر غير قابل للنقر
    self.btn.setEnabled(False)
    self.btn.setEnabled(True)

    # تغيير العنوان — أصلي Qt
    self.btn.setText("عنوان جديد")

    # التحقق من الحالة
    if self.btn.isEnabled():
        ...

## CLineEdit
### التعريف
CLineEdit هو حقل إدخال نص متوافق، يحل محل QLineEdit.

### لماذا؟
QLineEdit  يحتاج لسطر كود إضافي لإسترجاع النص .
CLineEdit يجعل هذا التفعيل تلقائيًا عبر الإشارة validated.

### الميزات
- الإشارة validated تُصدر بالنص الحالي عند كل Enter/Return.
- placeholderText كمعامل — يُعلن بواسطة NVDA عندما يكون الحقل فارغًا.
- العنوان عبر CLabel مع buddy.

### الاستخدام

    # PySide6
    from cwidgets.pyside6 import CLineEdit, CLabel
    # PyQt6
    from cwidgets.pyqt6 import CLineEdit, CLabel

    # إنشاء الحقل أولاً لـ buddy
    self.edit = CLineEdit(self)
    self.lbl  = CLabel("الاسم:", self, self.edit)
    layout.addWidget(self.lbl)
    layout.addWidget(self.edit)

    # مع نص مبدئي 
    self.edit = CLineEdit(self, "القاهرة")

    # مع نص إرشادي placeholder
    self.edit = CLineEdit(self, placeholderText="أدخل اسمك...")

    # إشارة validated
    self.edit.validated.connect(self.on_validated)

    def on_validated(self, text: str) -> None:
        text = self.edit.text()  # استرداد أصلي Qt
        print(text)

    # إظهار / إخفاء — أصلي Qt
    self.edit.hide()
    self.edit.show()


## CComboBox

### التعريف
CComboBox هو قائمة منسدلة متوافقة، يحل محل QComboBox.

### لماذا؟
- QComboBox الأصلي يتم التفعيل داخله بواسطة الأسهم .
و هذا يمثل مشكلة للمكفوفين الذين يتنقلون بالإسهم .

### الحل
فصل صريح بين التنقل والتفعيل .
مع المحافظة على التوافقية حتى في حالة تعطيل القائمة .

### الميزات
- التنقل الحر: ↑ ↓ للتنقل بدون تفعيل .
- التفعيل الصريح: Enter، Return، Space → بواسطة إشارة validated.
- الإشارة cleared: تُصدر عندما يتحقق المستخدم من قائمة فارغة.
- التعطيل المتاح: يعلن NVDA "غير متاح".
- العنوان عبر CLabel مع buddy — لا يُنصح باستخدام setAccessibleName لأنه يحل محل الملصق.

### الاستخدام

    # PySide6
    from cwidgets.pyside6 import CComboBox, CLabel, CMessageBox, CButton
    # PyQt6
    from cwidgets.pyqt6 import CComboBox, CLabel, CMessageBox, CButton

    # إنشاء القائمة أولاً لـ buddy
    self.combo = CComboBox(self)
    self.combo.addItems(["مصر", "تونس", "المغرب"])
    self.lbl = CLabel("قائمة الدول:", self, self.combo)
    layout.addWidget(self.lbl)
    layout.addWidget(self.combo)

    self.combo.validated.connect(self.on_selection)
    self.combo.cleared.connect(self.on_cleared)

    # زر يفرغ القائمة
    self.btn_clear = CButton("تفريغ", self)
    self.btn_clear.clicked.connect(self.combo.clear)

    def on_selection(self) -> None:
        text  = self.combo.currentText()
        index = self.combo.currentIndex()
        CMessageBox.information(self, "التحديد", f"الدولة: {text}")

    def on_cleared(self) -> None:
        CMessageBox.warning(self, "تحذير", "لا توجد عناصر متاحة في القائمة.")

    # تعطيل / إعادة تفعيل
    self.combo.setEnabled(False)
    self.combo.setEnabled(True)

## CListWidget

### التعريف
CListWidget هي قائمة متوافقة ، تحل محل QListWidget.

### لماذا؟
QListWidget الأصلي يتم التفعيل داخله فورًا عند التنقل باستخدام الأسهم.
و هذا يمثل عائقا للمكفوفين و تعطيل هذا التفعيل بالأسهم يتطلب كتابة أسطر كودية إضافية .
### الحل
- فصل بين التنقل والتفعيل .
-الحفاظ على إمكانية الوصول في وضع التعطيل.

### الميزات
- التنقل الحر: ↑ ↓ للتنقل بدون تفعيل .
- التفعيل الصريح: Enter، Return، Space.
- في حالة التعطيل : يعلن NVDA "غير متاح".
- العنوان عبر CLabel مع buddy — لا يُنصح باستخدام setAccessibleName لأنه يحل محل الملصق.

### الاستخدام

    # PySide6
    from cwidgets.pyside6 import CListWidget, CLabel
    # PyQt6
    from cwidgets.pyqt6 import CListWidget, CLabel

    # إنشاء القائمة
    self.list = CListWidget(self)
    self.list.addItems(["العراق", "السعودية", "الكويت"])
    self.lbl = CLabel("قائمة الدول:", self, self.list)
    layout.addWidget(self.lbl)
    layout.addWidget(self.list)

    # إشارة أصلية Qt — مطابقة لـ QListWidget
    self.liste.itemActivated.connect(self.on_item)

    def on_item(self, item) -> None:
        text = item.text()
        row  = self.liste.currentRow()
        print(row, text)

    # تعطيل / إعادة تفعيل
    self.liste.setEnabled(False)
    self.liste.setEnabled(True)

    # تفريغ — أصلي Qt
    self.liste.clear()

## CMessageBox

### التعريف
CMessageBox هي محاورة رسائل متوافقة.
### لماذا؟
QMessageBox الأصلي لا يوفر إغلاقًا تلقائيًا .
نحتاجه للرسائل التي لا تتطلب تدخلا من المستخدم .

### الحل
إضافة وضع تغلق فيه الرسالة بعد زمن محدد .

### الميزات
- information: مؤقت أو غير مؤقت — بدون صوت.
- warning: مؤقت أو غير مؤقت — بدون صوت.
- critical: دائمًا غير مؤقت + صوت النظام — إغلاق يدوي إلزامي.
- الإغلاق اليدوي ممكن دائمًا قبل انتهاء المهلة.

### الاستخدام

    # PySide6
    from cwidgets.pyside6 import CMessageBox
    # PyQt6
    from cwidgets.pyqt6 import CMessageBox

    # معلومات غير مؤقتة
    CMessageBox.information(self, "نجاح", "تم حفظ الملف.")

    # معلومات مؤقتة — إغلاق تلقائي بعد 3 ثوانٍ
    CMessageBox.information(self, "نجاح", "تم حفظ الملف.", timeout=3000)

    # تحذير غير مؤقت
    CMessageBox.warning(self, "تحذير", "مساحة القرص غير كافية.")

    # تحذير مؤقت
    CMessageBox.warning(self, "تحذير", "الاتصال غير مستقر.", timeout=4000)

    # خطأ — غير مؤقت + صوت — إغلاق يدوي إلزامي
    CMessageBox.critical(self, "خطأ", "الملف غير موجود.")

    # يُنصح باستخدام المهلة فقط لـ information و warning
    # المهلة غير متاحة لـ critical

## أفضل الممارسات

1 — العناوين: استخدم دائمًا CLabel مع buddy .

    # غير منصوح به — يحل محل label
    self.combo.setAccessibleName("...")

    # صحيح
    self.lbl = CLabel("قائمة الدول:", self, self.combo)

2 — التعطيل: setEnabled(False) متاح افتراضيًا على جميع المكونات C*.

3 — التفعيل:
- CLineEdit و CComboBox → إشارة validated
- CListWidget → إشارة أصلية Qt itemActivated

4 — ترتيب الإنشاء مع buddy: قم دائمًا بإنشاء العنصر قبل CLabel الخاص به.

    # صحيح — العنصر يُنشأ قبل الملصق
    self.combo = CComboBox(self)
    self.lbl   = CLabel("الدولة:", self, self.combo)

## متطلبات التشغيل 

- PySide6 أو PyQt6
- pywin32 — فقط لـ CTextEdit (دمج Win32 RichEdit)

المقدمة من المكتبة:
- validate_parent — التحقق المنتظم من النافذة parent
- logger — تسجيل الأخطاء (الوحدة "cwidgets")

##حدود المكتبة

- CTextEdit يعتمد على Win32 RichEdit — متوافق مع Windows فقط.
- لا يُنصح باستخدام setAccessibleName مع CComboBox و CListWidget لأنه يحل محل buddy CLabel.
- CButton: التظليل الرمادي عبر stylesheet — Windows لا يقوم بتظليل الزر تلقائيًا عند الحفاظ عليه نشطًا لـ NVDA.

## المطوّر :
محمد الهادي بالطيب)تونس(
للتواصل و التفاعل :
البريد الإلكتروني : hedidouz@gmail.com 
تاريخ تصميم المكتبة : ماي 2026 .


## الخاتمة

يهدف هذا المشروع إلى جعل تطبيقات Qt متاحة بنسبة 100% للمطورين والمستخدمين المكفوفين، دون التضحية بالإنتاجية أو عادات مطوري Qt.
