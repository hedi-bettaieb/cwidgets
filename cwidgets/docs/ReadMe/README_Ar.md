# دليل المستخدم - مكتبة CWidgets V0.1.3

## المقدمة

CWidgets هي مكتبة بايثون متخصصة تمنح المطورين المكفوفين
تحكمًا كاملاً في واجهات PyQt6 و PySide6.

لقد انتهت حقبة القيود مع QTextEdit — يمكنك الآن تصميم
واجهات تحتوي على مناطق تحرير متعددة الأسطر بحرية وتوافق كامل مع NVDA.

كل ما عليك فعله هو استبدال الحرف الأول (C بدلاً من Q):
- CTextEdit بدلاً من QTextEdit
- CButton بدلاً من QPushButton
- حيث تعني C مخصصة (Custom)

تدعم المكتبة بيئتي Qt:

# PySide6
from cwidgets.pyside6 import CButton, CLabel, CLineEdit

# PyQt6
from cwidgets.pyqt6 import CButton, CLabel, CLineEdit

CWidgets: برمج بثقة، صمّم بلا حدود.

## المكونات المتاحة

7 مكونات مخصصة متوافقة بالكامل مع NVDA:

1. CTextEdit
2. CButton
3. CLabel
4. CLineEdit
5. CComboBox
6. CListWidget
7. CMessageBox

## التثبيت

pip install cwidgets

## الوصول إلى المساعدة

import cwidgets

# قائمة بجميع المكونات المتاحة
cwidgets.widgets()

# قائمة بجميع الأقسام المتاحة
cwidgets.sections()

# فتح الدليل الكامل في المتصفح
cwidgets.show_help()
cwidgets.show_help(lang="fr")
cwidgets.show_help(lang="ar")

# فتح مكون معين مباشرة
cwidgets.show_help(lang="fr", goto="CButton")
cwidgets.show_help(lang="fr", goto="CTextEdit")

# فتح قسم معين مباشرة
cwidgets.show_help(lang="fr", goto="introduction")
cwidgets.show_help(lang="fr", goto="installation")

# واجهة برمجة التطبيقات لـ CTextEdit — العرض من الطرفية
cwidgets.ctextedit.show()          # الأسماء فقط
cwidgets.ctextedit.show_details()  # الأسماء + الأوصاف

## المشاكل الشائعة التي تم حلها

**CTextEdit** — منطقة تحرير متعددة الأسطر: يحل مشكلة عدم توافق QTextEdit مع NVDA.

**CComboBox & CListWidget** — فصل التنقل/التفعيل: يتجنب التفعيلات
غير المقصودة أثناء التنقل باستخدام مفاتيح الأسهم. يتم الحفاظ على إمكانية الوصول لـ NVDA
حتى في الوضع المعطل.

**CButton** — التفعيل عبر Enter، وBackspace، وSpace والنقر. التوافق مع NVDA
حتى عند التعطيل.

**CLabel** — تحسين التوافق للعناوين والملصقات.

**CLineEdit** — استرداد النص عبر Enter دون الحاجة إلى كتابة كود إضافي.

**CMessageBox** — مربعات حوار تغلق تلقائيًا مع تأخير قابل للتكوين.

باستثناء CTextEdit، ترث جميع المكونات من Qt وتحتفظ
بجميع خصائصها ووظائفها الأصلية.

## تفاصيل المكونات

## CTextEdit

### التعريف
CTextEdit هي منطقة تحرير متعددة الأسطر متوافقة بالكامل مع NVDA،
تعتمد على محرك Win32 RichEdit الأصلي.

### لماذا — المشكلة الأساسية
- QTextEdit الأصلي في Qt غير متوافق مع NVDA.
- لا يمكن للمطورين المكفوفين قراءة أو كتابة في هذا العنصر.
- حتى ظهور هذه المكتبة، لم تكن هناك حلول معروفة.

### الحل — RichEdit Win32 مدمج في Qt
يدمج الحل مباشرة عنصر تحكم RichEdit Win32 في نافذة Qt.
RichEdit Win32 متوافق أصلاً مع NVDA.

البنية الداخلية:
- CTextEdit — واجهة Qt العامة
- EditorStyle — الأنماط، الخط، اللون، المحاذاة
- RichEdit Win32 — المحرك الأصلي المتوافق مع NVDA

### الميزات
- إمكانية وصول كاملة لـ NVDA: القراءة، الكتابة، التنقل، التحديد.
- واجهة برمجة تطبيقات موسعة: 25 طريقة عامة متاحة.
- نص منسق: الخط، الحجم، غامق، مائل، اللون، المحاذاة.
- الإشارات: textChanged، selectionChanged، cursorPositionChanged.
- إدارة غير متزامنة: الأنماط والنص يتم وضعها في قائمة الانتظار قبل التهيئة.
- التركيز الذكي: يتم استعادته تلقائيًا بعد Alt+Tab.

### الاستيراد

# PySide6
from cwidgets.pyside6 import CTextEdit
# PyQt6
from cwidgets.pyqt6 import CTextEdit

### الإنشاء

self.editor = CTextEdit(self, accessible_name="اسم المنطقة")
layout.addWidget(self.editor)

### واجهة برمجة التطبيقات المتاحة

# عرض جميع الطرق من الطرفية
import cwidgets
cwidgets.ctextedit.show()          # الأسماء فقط
cwidgets.ctextedit.show_details()  # الأسماء + الأوصاف

# من الكود
CTextEdit.api()

### المحتوى

# تعيين المحتوى
self.editor.setText("مرحبًا!")

# استرداد المحتوى
text = self.editor.toPlainText()
text = self.editor.text()          # اسم مستعار لـ toPlainText()

# إضافة نص في النهاية
self.editor.append("سطر جديد.")

# إدراج في موضع المؤشر
self.editor.insertPlainText("نص مُدرج\n")

# إدراج HTML في موضع المؤشر
# يتم إزالة العلامات، <br> و <p> تصبح فواصل أسطر
self.editor.insertHtml("<p>مرحبًا <b>عالم</b></p>")  # يُدرج: "مرحبًا عالم"
self.editor.insertHtml("<p>السطر 1</p><br/>السطر 2")   # يُدرج: "السطر 1\nالسطر 2"

# مسح المحتوى
self.editor.clear()

### التحديد

# تحديد الكل
self.editor.selectAll()

# استرداد النص المحدد (يُرجع "" إذا لم يكن هناك تحديد)
text = self.editor.selectedText()

# مثال مُدمج — استرداد كل النص
self.editor.selectAll()
text = self.editor.selectedText()

### الخصائص

# عدد الأسطر
count = self.editor.lineCount()

# للقراءة فقط
self.editor.setReadOnly(True)    # تفعيل
self.editor.setReadOnly(False)   # تعطيل
state = self.editor.isReadOnly() # التحقق

### التنسيق

# الخط — QFont أو (الاسم، الحجم، غامق، مائل)
self.editor.setFont("Arial", 12, True, False)

# لون النص — الاسم أو (R, G, B)
self.editor.setTextColor("red")
self.editor.setTextColor((255, 0, 0))

# لون الخلفية
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

# أو RGB
(255, 0, 0)    # أحمر
(0, 128, 255)  # أزرق فاتح

### الحافظة

# تعمل الاختصارات Ctrl+C/X/V/Z/Y أصلاً عبر لوحة المفاتيح.
# تسمح هذه الطرق بالاستخدام البرمجي (مثلاً عبر زر).

self.editor.copy()   # نسخ التحديد
self.editor.cut()    # قص التحديد
self.editor.paste()  # لصق
self.editor.undo()   # تراجع
self.editor.redo()   # إعادة

### الإشارات

# الاستجابة للتغييرات في الوقت الفعلي
self.editor.textChanged.connect(self.on_text_changed)
self.editor.cursorPositionChanged.connect(self.on_cursor_changed)
self.editor.selectionChanged.connect(self.on_selection_changed)

def on_text_changed(self):
    print(self.editor.toPlainText())

def on_cursor_changed(self):
    print("تم تحريك المؤشر")

def on_selection_changed(self):
    print(self.editor.selectedText())

### السلوك في التخطيطات

لدى CTextEdit حجم أدنى يبلغ 50x50 بكسل لضمان رؤيته.

**الحالة 1 — QVBoxLayout (المحرر وحده في سطره)**
layout.addWidget(self.editor)

**الحالة 2 — QHBoxLayout مشترك مع QListWidget أو QComboBox**
بدون `stretch=1`، تأخذ المكونات الأخرى كل المساحة.
layout = QHBoxLayout()
layout.addWidget(self.list_widget, 1)
layout.addWidget(self.editor, 1)

**الحالة 3 — أبعاد ثابتة**
self.editor = CTextEdit(self, width=400, height=200)

**الحالة 4 — إخفاء / إظهار**
self.editor.hide()  # يخفي دون تدمير المحتوى
self.editor.show()  # يعيد العرض مع المحتوى سليمًا

### العنوان المرئي الاختياري

يتم قراءة accessible_name بواسطة NVDA لكنه غير مرئي بصريًا.
لإضافة عنوان مرئي، استخدم CLabel قبل المحرر في التخطيط:

self.editor = CTextEdit(self)
self.lbl    = CLabel("منطقة التحرير:", self, self.editor)
layout.addWidget(self.lbl)
layout.addWidget(self.editor)


## CLabel

### التعريف
CLabel هي ملصقة متوافقة مع NVDA تحل محل QLabel.

### لماذا؟
QLabel غير مرئي لـ NVDA إلا إذا كان مرتبطًا بـ buddy — وفقط
عندما يكون هذا الـ buddy لديه التركيز.

### الحل
- الوضع البسيط: متوافق مع NVDA، يتم التعرف عليه عبر التنقل بالتبويب.
- وضع الـ buddy: مرتبط بعنصر آخر، يُعلن عنه عندما يكون هذا العنصر لديه التركيز.

### الميزات
- تنظيف الاختصارات: `&Name` → "Name" لـ NVDA، مع الحفاظ على الاختصار المرئي.
- البادئة (prefix): نص إضافي للتعبير عن الحالة.
- المزامنة التلقائية عبر `setText()` و `setPrefix()`.

### الاستخدام

# PySide6
from cwidgets.pyside6 import CLabel, CLineEdit
# PyQt6
from cwidgets.pyqt6 import CLabel, CLineEdit

# الوضع البسيط
self.lbl = CLabel("تم حفظ الملف", self)

# مع بادئة — NVDA يعلن: "حالة تم حفظ الملف"
self.lbl = CLabel("تم حفظ الملف", self, prefix="حالة")

# وضع الـ buddy
self.edit = CLineEdit(self)
self.lbl  = CLabel("الاسم:", self, self.edit)
layout.addWidget(self.lbl)
layout.addWidget(self.edit)

# التحديث الديناميكي
self.lbl.setText("جاري المعالجة")
self.lbl.setPrefix("خطأ")


## CButton

### التعريف
CButton هو زر يمكن الوصول إليه يحل محل QPushButton.

### لماذا؟
- QPushButton يقبل فقط شريط المسافة — يتم تجاهل Enter و Backspace.
- setEnabled(False) يجعل الزر غير مرئي لـ NVDA.

### الحل
- التفعيل عبر Enter، وBackspace، وSpace والنقر بالماوس.
- الوضع المعطل: غير قابل للنقر لكنه مرئي لـ NVDA ("غير متاح").

### الميزات
- تفعيل موسع: Space، Enter، Backspace، النقر بالماوس.
- التعطيل المتاح: NVDA يعلن "غير متاح".
- واجهة برمجة تطبيقات مطابقة لـ QPushButton.

### الاستخدام

# PySide6
from cwidgets.pyside6 import CButton
# PyQt6
from cwidgets.pyqt6 import CButton

self.btn = CButton("حفظ", self)
self.btn.clicked.connect(self.on_click)

# تعطيل / إعادة تفعيل
self.btn.setEnabled(False)
self.btn.setEnabled(True)

# التحقق من الحالة
if self.btn.isEnabled():
    ...

## CLineEdit

### التعريف
CLineEdit هو حقل إدخال متوافق يحل محل QLineEdit.

### لماذا؟
يتطلب QLineEdit كتابة كود إضافي لاسترداد النص عند التحقق.
يقوم CLineEdit بأتمتة ذلك عبر الإشارة `validated`.

### الميزات
- الإشارة `validated`: ترسل النص عند كل Enter/Backspace.
- `placeholderText` كمعامل، يُعلن عنه بواسطة NVDA عندما يكون الحقل فارغًا.
- العنوان عبر CLabel مع buddy.

### الاستخدام

# PySide6
from cwidgets.pyside6 import CLineEdit, CLabel
# PyQt6
from cwidgets.pyqt6 import CLineEdit, CLabel

self.edit = CLineEdit(self)
self.lbl  = CLabel("الاسم:", self, self.edit)
layout.addWidget(self.lbl)
layout.addWidget(self.edit)

# مع نص أولي
self.edit = CLineEdit(self, "القاهرة")

# مع نص نائب
self.edit = CLineEdit(self, placeholderText="أدخل اسمك...")

# إشارة validated
self.edit.validated.connect(self.on_validated)

def on_validated(self, text: str) -> None:
    print(text)

## CComboBox

### التعريف
CComboBox هي قائمة منسدلة يمكن الوصول إليها تحل محل QComboBox.

### لماذا؟
يقوم QComboBox بتفعيل العنصر أثناء التنقل باستخدام مفاتيح الأسهم —
مشكل للمستخدمين المكفوفين.

### الحل
فصل صريح بين التنقل (الأسهم) والتفعيل (Enter/Space).
الحفاظ على إمكانية الوصول لـ NVDA في الوضع المعطل.

### الميزات
- التنقل الحر: ↑↓ دون تفعيل.
- التفعيل الصريح: Enter، Backspace، Space → إشارة `validated`.
- الإشارة `cleared`: تُرسل إذا تفاعل المستخدم مع قائمة فارغة.
- التعطيل المتاح: NVDA يعلن "غير متاح".

### الاستخدام

# PySide6
from cwidgets.pyside6 import CComboBox, CLabel, CMessageBox
# PyQt6
from cwidgets.pyqt6 import CComboBox, CLabel, CMessageBox

self.combo = CComboBox(self)
self.combo.addItems(["مصر", "تونس", "المغرب"])
self.lbl = CLabel("الدولة:", self, self.combo)
layout.addWidget(self.lbl)
layout.addWidget(self.combo)

self.combo.validated.connect(self.on_selection)
self.combo.cleared.connect(self.on_cleared)

def on_selection(self) -> None:
    text  = self.combo.currentText()
    index = self.combo.currentIndex()
    CMessageBox.information(self, "اختيار", f"الدولة: {text}")

def on_cleared(self) -> None:
    CMessageBox.warning(self, "تحذير", "القائمة فارغة.")

# تعطيل / إعادة تفعيل
self.combo.setEnabled(False)
self.combo.setEnabled(True)

## CListWidget

### التعريف
CListWidget هي قائمة يمكن الوصول إليها تحل محل QListWidget.

### لماذا؟
يقوم QListWidget بتفعيل العنصر فورًا أثناء التنقل —
عائق للمستخدمين المكفوفين.

### الحل
فصل بين التنقل والتفعيل. إمكانية الوصول لـ NVDA في الوضع المعطل.

### الميزات
- التنقل الحر: ↑↓ دون تفعيل.
- التفعيل الصريح: Enter، Backspace، Space.
- التعطيل المتاح: NVDA يعلن "غير متاح".

### الاستخدام

# PySide6
from cwidgets.pyside6 import CListWidget, CLabel
# PyQt6
from cwidgets.pyqt6 import CListWidget, CLabel

self.liste = CListWidget(self)
self.liste.addItems(["العراق", "السعودية", "الكويت"])
self.lbl = CLabel("الدولة:", self, self.liste)
layout.addWidget(self.lbl)
layout.addWidget(self.liste)

self.liste.itemActivated.connect(self.on_item)

def on_item(self, item) -> None:
    text = item.text()
    row  = self.liste.currentRow()
    print(row, text)

# تعطيل / إعادة تفعيل
self.liste.setEnabled(False)
self.liste.setEnabled(True)

# إفراغ
self.liste.clear()

## CMessageBox

### التعريف
CMessageBox هي مربع حوار يمكن الوصول إليه يحل محل QMessageBox.

### لماذا؟
لا يقدم QMessageBox إغلاقًا تلقائيًا.

### الحل
إضافة وضع مؤقت مع إغلاق تلقائي بعد تأخير.

### الميزات
- `information`: مؤقت أو غير مؤقت، بدون صوت.
- `warning`: مؤقت أو غير مؤقت، بدون صوت.
- `critical`: دائمًا غير مؤقت + صوت النظام، يتطلب إغلاقًا يدويًا.
- الإغلاق اليدوي ممكن دائمًا قبل انتهاء المهلة.

### الاستخدام

# PySide6
from cwidgets.pyside6 import CMessageBox
# PyQt6
from cwidgets.pyqt6 import CMessageBox

# معلومات
CMessageBox.information(self, "نجاح", "تم حفظ الملف.")
CMessageBox.information(self, "نجاح", "تم حفظ الملف.", timeout=3000)

# تحذير
CMessageBox.warning(self, "تحذير", "مساحة القرص غير كافية.")
CMessageBox.warning(self, "تحذير", "اتصال غير مستقر.", timeout=4000)

# خطأ — إغلاق يدوي + صوت
CMessageBox.critical(self, "خطأ", "الملف غير موجود.")

## الممارسات الجيدة

**1 — العناوين: استخدم دائمًا CLabel مع buddy**
# غير موصى به
self.combo.setAccessibleName("...")

# صحيح
self.lbl = CLabel("الدولة:", self, self.combo)

**2 — التعطيل**: `setEnabled(False)` متاح على جميع مكونات C*.

**3 — التفعيل**
- CLineEdit و CComboBox → إشارة `validated`
- CListWidget → إشارة `itemActivated`

**4 — ترتيب الإنشاء مع buddy**: قم دائمًا بإنشاء العنصر قبل CLabel الخاص به.
self.combo = CComboBox(self)
self.lbl   = CLabel("الدولة:", self, self.combo)

## متطلبات النظام

- PySide6 أو PyQt6
- pywin32 — فقط لـ CTextEdit (تكامل Win32 RichEdit)
- Windows فقط لـ CTextEdit

## القيود

- CTextEdit: Windows فقط (يعتمد على Win32 RichEdit).
- CComboBox و CListWidget: لا يُنصح بـ `setAccessibleName` — يستبدل CLabel buddy.
- CButton: ظل رمادي عبر stylesheet — لا يقوم Windows تلقائيًا
  بتظليل الزر النشط لـ NVDA.

## المطور

محمد الهادي بتايب (تونس)
البريد الإلكتروني: hedidouz@gmail.com
تاريخ التصميم: مايو 2026

## الخاتمة

تهدف CWidgets إلى جعل تطبيقات Qt متوافقة بنسبة 100% مع المطورين
والمستخدمين المكفوفين، دون التضحية بالإنتاجية أو عادات Qt.