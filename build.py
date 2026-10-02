"""Build the separate HS Computer Science revision page from its initial notes page.
The initial PDF-based sections remain in base.html; this generator adds researched lessons.
"""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).parent
base = (ROOT / 'base.html').read_text(encoding='utf-8')

def code(s):
    # Code in Python triple-quoted strings can lose the slash in C's \\n escape.
    # Normalize only the known accidental quote+newline+quote sequence.
    s = s.strip().replace('"\n"', '"\\n"')
    return '<pre><code>' + escape(s) + '</code></pre>'

def box(title, body, tag=''):
    return '<details class="card"><summary>' + title + (' <span class="pill">'+tag+'</span>' if tag else '') + '</summary><div class="answer">' + body + '</div></details>'

def flow(items):
    return '<div class="flow" role="img" aria-label="' + escape(' then '.join(items), quote=True) + '">' + ''.join('<span class="node">'+escape(x)+'</span>' + ('<span aria-hidden="true" class="arrow">→</span>' if i<len(items)-1 else '') for i,x in enumerate(items)) + '</div>'

intro = '''<section id="map"><h2>Start here / What to study first</h2><p class="sub">A focused order for this half-yearly, then the wider board syllabus.</p>
<div class="callout"><strong>Scope matters:</strong> the existing study plan names <strong>OOP in C++ and DBMS/SQL</strong> for this half-yearly. The supplied main-notes PDF adds <strong>networks</strong> and lists data structures, errors and operators without detail. The official HS final-year syllabus also covers data structures, Boolean algebra and networks, but it does <em>not</em> confirm your school’s half-yearly chapter boundaries. Ask your teacher which of these extra units are included. The official syllabus is for the <em>final-year course</em>, not a 50-mark half-yearly blueprint. <a href="#sources">Sources</a>.</div>
<div class="grid"><div class="tile"><b>01 · First priority</b><p>Class → object → access control → constructor/destructor → inheritance → polymorphism. Write and trace Turbo C++ programs.</p></div><div class="tile"><b>02 · First priority</b><p>DBMS vocabulary → keys and constraints → CREATE/ALTER → INSERT/UPDATE/DELETE → SELECT, conditions, grouping, joins.</p></div><div class="tile"><b>03 · Your PDF’s focus</b><p>LAN/MAN/WAN, topologies, devices, bandwidth, SQL data types, BOOK/PUBLISHER and ITEM query practice.</p></div><div class="tile"><b>04 · Check with teacher</b><p>Data structures and Boolean algebra occur in the full HS course; short bridges appear here, not as confirmed half-yearly units.</p></div></div>
<p class="small">“ASSEB-inspired” below means <strong>original practice questions</strong> in short/long/program/query styles, not an official paper or a predicted paper. Labels such as 1m/2m/4m are practice targets, not an authenticated 2026 half-yearly mark scheme.</p></section>
<section id="concepts"><h2>01 / Important points &amp; concept map</h2><p class="sub">Read this once before opening the detailed notes.</p>
<ul><li><b>Class</b> is a blueprint; an <b>object</b> is an instance. <b>Encapsulation</b> keeps data and methods together; private data gives controlled access.</li><li><b>Constructor</b> initializes a new object automatically. <b>Destructor</b> runs when an object’s lifetime ends. Function overloading is an example of compile-time polymorphism.</li><li><b>Inheritance</b> extends a base class. With public inheritance, public stays public and protected stays protected in the derived class; base private members remain inaccessible directly.</li><li><b>Database</b> organizes related records. A relation is a table, tuple a row, attribute a column, domain allowed values; a primary key uniquely identifies a row.</li><li><b>DDL</b> changes structures; <b>DML</b> changes data. <code>WHERE</code> filters rows before groups; <code>HAVING</code> filters groups after <code>GROUP BY</code>.</li><li><b>Binary search</b> requires a sorted array. Stack uses LIFO; queue uses FIFO. These are full-syllabus topics, not confirmed half-yearly topics.</li></ul>
<h3>Flowchart: object life cycle</h3>''' + flow(['Define class','Create object','Constructor runs','Use methods','Object leaves scope','Destructor runs']) + '''
<h3>Flowchart: write a SQL query</h3>''' + flow(['Pick table(s)','SELECT columns','FROM table','WHERE rows','GROUP BY groups','HAVING groups','ORDER BY result']) + '''<p class="small">These are conceptual flowcharts, not a diagram of how every DBMS physically executes a query. Omit unneeded clauses; <code>HAVING</code> is normally used with grouping.</p>
<h3>Flowchart: network question</h3>''' + flow(['How large is the area?','Building → LAN','City → MAN','Wide area → WAN']) + '''</section>
<section id="turbo"><h2>02 / Turbo C vs Turbo C++</h2><p class="sub">Important correction before writing programs.</p><div class="callout"><strong>Turbo C and Turbo C++ are not the same language.</strong> Your official Class XII subject specifies <strong>object-oriented programming in C++</strong> and its file-handling section explicitly mentions <code>fstream.h</code>. Classes, constructors and inheritance cannot be written as C programs. Accordingly the OOP examples here are <strong>old-style Turbo C++ (.CPP)</strong>; the procedural examples are <strong>Turbo C (.C)</strong>. Ask your teacher which compiler/version is actually installed. These examples have been syntax-checked using a modern compiler in compatible form where possible, but no Turbo compiler was available here for direct testing. [1]</div>
<p><b>For .CPP:</b> <code>#include &lt;iostream.h&gt;</code>, <code>cout/cin</code>, <code>int main()</code> and <code>return 0;</code>; no <code>using namespace std</code>, templates or modern features. For .C use <code>#include &lt;stdio.h&gt;</code>, <code>printf/scanf</code>. <code>conio.h</code>, <code>clrscr()</code> and <code>getch()</code> are optional Borland-specific console conveniences, not required for program logic. Avoid <code>void main()</code> as non-standard.</p>
''' + box('How do I save and run the sample programs?', '<p>Save C++ snippets as <code>.CPP</code> and C snippets as <code>.C</code>. In Turbo C++ IDE, compile then run. If the display disappears quickly, view the output screen using the IDE’s output-window shortcut or add <code>#include &lt;conio.h&gt;</code> and <code>getch();</code> just before <code>return 0;</code>. Do not copy several complete programs into one file: each contains its own <code>main()</code>.</p>') + '''</section>
<section id="oop"><h2>03 / OOP in C++ · lessons and examples</h2><p class="sub">Official course unit I; the half-yearly study plan explicitly prioritises this unit. [1]</p>
''' + box('Class, object, visibility and encapsulation', '<p>Declare a <b>class</b> with data members and member functions. A class’s members are <b>private by default</b>. Expose safe public functions rather than changing private data directly. An object occupies storage as an instance of the class. <code>::</code> defines a member function outside its class.</p>' + code('''#include <iostream.h>
class Item {
    int price;               // private by default
public:
    void setPrice(int p);
    int getPrice() { return price; }
};
void Item::setPrice(int p) { price = p; }
int main() {
    Item pen;
    pen.setPrice(20);
    cout << "Price = " << pen.getPrice() << "\\n";
    return 0;
}''') + '<p><b>Output:</b> Price = 20. You cannot write <code>pen.price = 20</code> outside the class because <code>price</code> is private.</p>') + '''
''' + box('Constructor, overloaded constructors, copy constructor, destructor', '<p>A <b>constructor</b> has the class name and no return type; it runs when an object is created. A no-argument constructor is a default constructor. Constructors may be overloaded by parameter list; a copy constructor builds an object from another of the same class. A <b>destructor</b> starts with <code>~</code>, has no parameters/return type, and is called when an automatic object leaves scope.</p>' + code('''#include <iostream.h>
class Box {
    int length;
public:
    Box() { length = 0; }
    Box(int n) { length = n; }
    Box(const Box &other) { length = other.length; }
    ~Box() { } // cleanup if needed
    int getLength() { return length; }
};
int main() {
    Box a(7);
    Box b(a);
    cout << b.getLength() << "\\n";
    return 0;
}''') + '<p><b>Output:</b> 7. <code>Box b(a)</code> calls the copy constructor.</p>') + '''
''' + box('Inheritance and protected members', '<p>A <b>derived class</b> inherits accessible base members. <b>Single</b>: one base; <b>multilevel</b>: A → B → C; <b>multiple</b>: two or more bases for one derived class. Public inheritance keeps base public members public and protected members protected; base private members are not directly accessible in the derived class.</p>' + code('''#include <iostream.h>
class Person {
protected:
    int age;
public:
    void setAge(int a) { age = a; }
};
class Student : public Person {
public:
    void show() { cout << "Age: " << age << "\\n"; }
};
int main() {
    Student s;
    s.setAge(17);
    s.show();
    return 0;
}''') + '<p><b>Output:</b> Age: 17.</p>') + '''
''' + box('Function overloading = compile-time polymorphism', '<p>Functions with the same name can have different parameter lists; the call selects the matching version. Return type alone is <b>not</b> enough to overload a function.</p>' + code('''#include <iostream.h>
int area(int side) { return side * side; }
int area(int length, int width) { return length * width; }
int main() {
    cout << area(4) << " " << area(4, 5) << "\\n";
    return 0;
}''') + '<p><b>Output:</b> 16 20.</p>') + '''
''' + box('Pointers, references and new/delete', '<p>A pointer stores an address. <code>&amp;</code> takes an address; <code>*</code> dereferences it. A reference is another name for an existing variable. <code>new</code> allocates, and <code>delete</code> releases dynamically allocated storage. Never dereference an uninitialized pointer.</p>' + code('''#include <iostream.h>
int main() {
    int x = 10;
    int &alias = x;
    int *p = new int;
    *p = alias + 5;
    cout << *p << "\\n";
    delete p;
    return 0;
}''') + '<p><b>Output:</b> 15. A pointer to a structure/object can use <code>p-&gt;member</code>.</p>') + '''
''' + box('Text file handling · fstream.h', '<p>File streams persist data after the program ends: <code>ofstream</code> writes, <code>ifstream</code> reads; <code>ios::app</code> appends. Check a stream before using it. Read a line with <code>getline</code>. Binary files use <code>read</code>/<code>write</code>; do not write raw objects containing pointers or dynamic strings to binary files.</p>' + code('''#include <iostream.h>
#include <fstream.h>
int main() {
    ofstream out("NOTES.TXT");
    if (!out) { cout << "Open failed\\n"; return 1; }
    out << "Assam" << "\\n";
    out.close();
    ifstream in("NOTES.TXT");
    char line[80];
    if (!in) { cout << "Read failed\\n"; return 1; }
    while (in.getline(line, 80)) cout << line << "\\n";
    in.close();
    return 0;
}''') + '<p><b>Output:</b> Assam. Compiling as <code>.CPP</code> requires the old Turbo C++ header; modern compilers use <code>&lt;fstream&gt;</code> instead.</p>') + '''</section>
<section id="cprograms"><h2>04 / Turbo C programs (.C)</h2><p class="sub">Procedural revision: operators, errors and data structures mentioned in your notes or the full syllabus. These are C, <em>not</em> OOP. [1]</p>
''' + box('Operators + even/odd · branching flowchart', flow(['Read n','n % 2 == 0?','Yes → even','No → odd']) + code('''#include <stdio.h>
int main(void) {
    int n;
    printf("Enter a number: ");
    if (scanf("%d", &n) != 1) return 1;
    if (n % 2 == 0) printf("Even\\n");
    else printf("Odd\\n");
    return 0;
}''') + '<p><b>Example:</b> input 7 → Odd. <code>%</code> gives the remainder; <code>==</code> compares, while <code>=</code> assigns.</p>') + '''
''' + box('Linear search · loop flowchart', flow(['Start at index 0','Compare value','Match? → print index','Else advance','End → not found']) + code('''#include <stdio.h>
int main(void) {
    int a[5] = {4, 9, 2, 7, 1};
    int key = 7, i, found = -1;
    for (i = 0; i < 5; ++i) {
        if (a[i] == key) { found = i; break; }
    }
    if (found >= 0) printf("Found at index %d\\n", found);
    else printf("Not found\\n");
    return 0;
}''') + '<p><b>Output:</b> Found at index 3. Linear search does not require sorted input; binary search does.</p>') + '''
''' + box('Stack using an array · PUSH and POP', flow(['PUSH request','Is top at MAX−1?','Yes → overflow','No → increment top; store']) + code('''#include <stdio.h>
#define MAX 5
int stack[MAX], top = -1;
void push(int x) {
    if (top == MAX - 1) printf("Overflow\\n");
    else stack[++top] = x;
}
void pop(void) {
    if (top == -1) printf("Underflow\\n");
    else printf("Popped %d\\n", stack[top--]);
}
int main(void) {
    push(10); push(20); pop(); pop();
    return 0;
}''') + '<p><b>Output:</b> Popped 20; then Popped 10. This is an illustrative <code>.C</code> exercise; the official Class XII practical specifies C++ for its programming problem.</p>') + '''
''' + box('Three types of programming errors', '<ul><li><b>Syntax/compiler error:</b> missing semicolon or misspelled identifier; compilation fails.</li><li><b>Runtime error:</b> occurs while executing, e.g. invalid input or out-of-range access may fail or behave unpredictably.</li><li><b>Logical error:</b> runs but gives the wrong answer, e.g. using <code>+</code> where <code>*</code> was intended.</li></ul>') + '''</section>
<section id="dbms"><h2>05 / DBMS · detailed concepts</h2><p class="sub">Official course unit III; overlaps strongly with the supplied PDF. [1]</p>
''' + box('Database, DBMS, relation, attribute, tuple and domain', '<p>A <b>database</b> is organized related data; a <b>DBMS</b> creates, stores, retrieves and manages it. A relational <b>relation</b> is represented as a table; <b>attributes</b> are columns, <b>tuples</b> are rows, and a <b>domain</b> is a column’s allowed type/set of values. In ITEM, <code>Price</code> is an attribute and <code>(1, Pen, 20, 50)</code> is a tuple.</p>') + '''
''' + box('Candidate, primary, alternate and foreign keys', '<p>A <b>candidate key</b> can uniquely identify a row and has no unnecessary column; choose one as the <b>primary key</b>. Other candidate keys are <b>alternate keys</b>. A <b>foreign key</b> in BOOK points to a key in PUBLISHER. Primary keys are unique and not NULL. Foreign keys may repeat across rows and may be NULL unless explicitly constrained.</p>' + flow(['PUBLISHER.P_ID (primary)','BOOK.P_ID (foreign)','Valid P_ID or allowed NULL']) ) + '''
''' + box('Relational algebra &amp; SQL clauses', '<p><b>Selection</b> chooses rows (<code>WHERE</code>); <b>projection</b> chooses columns (<code>SELECT column</code>); <b>union</b> combines compatible result sets without duplicate tuples; <b>Cartesian product</b> forms all pairs. In SQL, <code>UNION</code> removes duplicate rows unless <code>UNION ALL</code> is used.</p>' + code('''SELECT Item_Name, Price FROM ITEM WHERE Price BETWEEN 10 AND 25;
SELECT DISTINCT Stock FROM ITEM ORDER BY Stock DESC;
SELECT Stock, COUNT(*) FROM ITEM
GROUP BY Stock HAVING COUNT(*) > 1;''') + '<p>Example of a two-table equi-join: </p>' + code('''SELECT B.Book_title, P.P_name
FROM BOOK B, PUBLISHER P
WHERE B.P_ID = P.P_ID;''')) + '''
''' + box('DDL vs DML, DELETE vs DROP, WHERE vs HAVING', '<p><b>DDL:</b> CREATE, ALTER, DROP change table definitions. <b>DML:</b> INSERT, UPDATE, DELETE change stored rows; SELECT retrieves them. <code>DELETE FROM ITEM WHERE Item_no = 4;</code> removes one selected row; <code>DROP TABLE ITEM;</code> removes the table itself. <code>WHERE</code> tests individual rows; <code>HAVING</code> tests groups/aggregate results.</p>') + '''</section>
'''

extra = '''<section id="wider"><h2>Full-board syllabus bridge · verify school scope</h2><p class="sub">These concepts occur in the official final-year syllabus, but are not confirmed by the half-yearly study-plan wording. [1]</p>
''' + box('Data structures: array, stack and queue', '<p><b>Array:</b> same-type values at indexed positions; insertion/deletion may require shifting. <b>Stack:</b> LIFO; PUSH adds to top, POP removes from top; check overflow/underflow. <b>Queue:</b> FIFO; insert at rear, remove at front. A circular queue wraps indices instead of wasting freed slots.</p>' + flow(['PUSH 10','PUSH 20','POP → 20','POP → 10'])) + '''
''' + box('Boolean algebra and network extras', '<p><b>AND</b> is true only if both inputs are true; <b>OR</b> if either is true; <b>NOT</b> reverses truth value. De Morgan: <code>NOT(A AND B) = (NOT A) OR (NOT B)</code>; <code>NOT(A OR B) = (NOT A) AND (NOT B)</code>. A <b>star</b> network has a central switch; a <b>bus</b> shares a backbone. A <b>switch</b> connects devices within a LAN; a <b>router</b> joins different networks. Bandwidth in Hz describes a channel’s frequency range; bit rate in bps describes data transfer rate—do not equate them.</p>') + '''</section>
<section id="questions"><h2>Original ASSEB-style practice · answered</h2><p class="sub">Inspired by the official unit topics and typical short/long/program/query forms; <strong>not copied from, approved by or predicted as an ASSEB paper</strong>. [1][2]</p>
'''
qa = [
('1m · What is the default access level in a C++ class?','<p><b>Private.</b> Members cannot be accessed directly from unrelated code unless declared public.</p>'),
('1m · Name the function called when an object is created.','<p><b>Constructor.</b> It has the same name as its class and no return type.</p>'),
('2m · Differentiate class and object.','<p>A class describes data and operations; an object is a particular instance of that class. For example, <code>class Book</code> defines a type, while <code>Book b;</code> creates an object.</p>'),
('2m · Explain encapsulation and data hiding.','<p>Encapsulation groups data and methods in one class. Data hiding restricts direct access to internal data, usually with private members and public methods.</p>'),
('2m · Constructor versus destructor: state two differences.','<p>A constructor initializes an object when created and has the class name; a destructor runs when its lifetime ends and has the name prefixed with <code>~</code>. Constructors may be overloaded; a class has only one destructor.</p>'),
('2m · What is a primary key? Can it be NULL?','<p>A primary key uniquely identifies each row. It cannot be NULL.</p>'),
('2m · What is a topology? Give one benefit of star topology.','<p>Topology is the physical or logical arrangement of network connections. In a star, one device’s cable failure usually does not disconnect the others.</p>'),
('2m · Expand LAN, MAN and WAN.','<p>Local Area Network, Metropolitan Area Network and Wide Area Network.</p>'),
('3m · Explain a foreign key using two tables.','<p><code>PUBLISHER(P_ID)</code> has primary key <code>P_ID</code>. <code>BOOK(P_ID)</code> may be a foreign key referencing it; this prevents a non-NULL BOOK publisher ID from pointing to a nonexistent publisher (when constraints are enforced).</p>'),
('3m · Contrast DROP TABLE and DELETE FROM.','<p><code>DROP TABLE</code> removes the whole table definition and its data. <code>DELETE FROM</code> removes rows but retains the table structure; add <code>WHERE</code> to target specific rows.</p>'),
('4m · Write queries for names, average price and low-stock items.','<p>Using <code>ITEM(Item_Name, Price, Stock)</code>:</p>'+code('''SELECT Item_Name, Price FROM ITEM;
SELECT AVG(Price) AS Average_Price FROM ITEM;
SELECT Item_Name FROM ITEM WHERE Stock < 50;''')+'<p>Given the PDF table, the average price is <b>15</b>, and low-stock items are Eraser and Sharpener.</p>'),
('4m · Write a group query and explain WHERE versus HAVING.','<p>To show stock values shared by more than one item:</p>'+code('''SELECT Stock, COUNT(*) AS Total
FROM ITEM
GROUP BY Stock
HAVING COUNT(*) > 1;''')+'<p>Output: stock <b>50</b>, total <b>2</b>. WHERE filters rows before grouping; HAVING filters the grouped results.</p>'),
('4m · Write a Turbo C++ class with private data and a public method.','<p>See the complete <a href="#oop">Item class program</a>. Its data member <code>price</code> is private; <code>setPrice()</code> and <code>getPrice()</code> are public. Output: <code>Price = 20</code>.</p>'),
('4m · Explain single and multilevel inheritance with an example.','<p><b>Single:</b> <code>class B : public A</code> (B derives from A). <b>Multilevel:</b> <code>class C : public B</code> where B already derives from A. C inherits accessible members along A → B → C. Private base members are not directly accessible.</p>'),
('4m · Why does a binary search need a sorted array?','<p>At each step binary search compares the middle element and discards half of the range based on order. Without sorted order, it cannot know which half to discard; use linear search instead.</p>'),
('4m · Trace stack PUSH(10), PUSH(20), POP(), PUSH(30).','<p>After first two pushes, stack is [10, 20] (20 at top). POP removes 20. PUSH(30) gives [10, 30]; top is 30.</p>'),
('5m · Write a Turbo C program to find a value in an array.','<p>Use the complete <a href="#cprograms">linear-search .C program</a>. For array {4,9,2,7,1} and key 7, it prints <code>Found at index 3</code>. Include the comparison loop and not-found branch in an exam answer.</p>'),
('5m · Build two tables with a primary/foreign key.','<p>See the complete <a href="#commands">PUBLISHER and BOOK DDL</a>. Create PUBLISHER first because BOOK references it. In BOOK, ISBN is the primary key and P_ID is the foreign key.</p>'),
]
extra += ''.join(box(q,a) for q,a in qa) + '</section>'
extra += '''<section id="sources"><h2>Sources &amp; coverage</h2><ul>
<li>[1] <a href="https://ahsec.assam.gov.in/wp-content/uploads/2022/03/2-Computer-Science-and-Application-1.pdf" target="_blank" rel="noopener">AHSEC, Computer Science and Application, HS Final Year syllabus (PDF)</a> · especially pp. 1–4. It lists full-course units, including C++ OOP, data structures, SQL, Boolean algebra and networking. It does <b>not</b> establish local half-yearly chapter boundaries.</li>
<li>[2] <a href="https://school.careers360.com/boards/ahsec/ahsec-question-papers" target="_blank" rel="noopener">Careers360, AHSEC question-paper listing</a> · used only to frame original question/answer practice, not to claim that these questions appeared in any actual paper.</li>
<li>[3] <em>Half Yearly Main Notes</em> · user-supplied, 8-page PDF. PDF-page references in the basic notes below refer to this document; it lists extra question topics but does not certify the half-yearly syllabus.</li>
<li>[4] Existing local <em>Computer Science &amp; Application · Focus</em> study plan · identifies OOP in C++ and DBMS/SQL as the half-yearly units, and states 50 marks. School-issued syllabus was not supplied; this is a planning source, not official confirmation.</li>
</ul><p class="small">Codes and flowcharts here are original study examples; output depends on the input and compiler version. No school or board endorsement is claimed.</p></section>'''

# Keep the original PDF-based notes, but put new high-priority concept lessons first.
base = base.replace('<title>Computer Science · Half-yearly main notes</title>', '<title>Computer Science · Complete half-yearly revision</title>')
base = base.replace('<header><h1>Computer Science<br>half-yearly main notes</h1><p>Clear, short answers from the supplied <em>Half Yearly Main Notes</em> PDF. Open any question to revise its answer. Page references point to that PDF; blue notes and corrections are editorial additions.</p></header>', '<header><h1>Computer Science<br>revision guide</h1><p>Important concepts first, then flowcharts, Turbo-compatible C and C++ programs, detailed notes and answered ASSEB-style practice. Your common-question PDF remains in the guide below.</p></header>')
oldnav = '<nav class="nav" aria-label="Jump to topic"><a href="#networks">Networks</a><a href="#sql">SQL basics</a><a href="#commands">SQL commands</a><a href="#practice">Query practice</a><a href="#topics">More topics</a><a href="#corrections">Source corrections</a></nav>'
newnav = '<nav class="nav" aria-label="Jump to topic"><a href="#map">Study map</a><a href="#concepts">Key points</a><a href="#turbo">Turbo setup</a><a href="#oop">C++ OOP</a><a href="#cprograms">C programs</a><a href="#dbms">DBMS</a><a href="#networks">Networks</a><a href="#sql">SQL notes</a><a href="#commands">SQL commands</a><a href="#practice">SQL practice</a><a href="#wider">Other units</a><a href="#questions">Questions</a><a href="#sources">Sources</a></nav>'
assert oldnav in base
base = base.replace(oldnav, newnav)
base = base.replace('<section id="networks">', intro + '<section id="networks">', 1)
base = base.replace('<section id="corrections">', extra + '<section id="corrections">', 1)
base = base.replace('not an official syllabus or question paper. Check facts, textbook wording and exam pattern with your teacher; no question is guaranteed.', 'not an official half-yearly syllabus or question paper. Verify the school’s chapter list, textbook wording and exam pattern with your teacher; no question is guaranteed.')
base = base.replace('made with love by aloopitika.', 'made with love by aloopitika')
base = base.replace('</style>', '''.flow{display:flex;align-items:center;gap:7px;flex-wrap:wrap;background:var(--soft);border:1px solid var(--line);padding:12px;border-radius:8px;margin:10px 0 20px}.node{background:#fff;border:1px solid #d9d6d2;padding:6px 9px;border-radius:6px;font-size:12px;font-weight:600}.arrow{color:var(--blue);font-weight:bold}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:11px;margin:18px 0}.tile{border:1px solid var(--line);border-radius:9px;padding:14px}.tile p{margin:5px 0 0;color:var(--muted);font-size:13px}@media(max-width:600px){.grid{grid-template-columns:1fr}}html{scroll-padding-top:8px}a:focus-visible,summary:focus-visible{outline:2px solid var(--blue);outline-offset:2px}</style>''')
# A distinct learning path: theory, practical lab, original questions and recap.
base = base.replace('<section id="networks">', '<h2 class="part-head">Theory study · networks and SQL from your notes</h2><section id="networks">', 1)
base = base.replace('<section id="wider">', '<h2 class="part-head">Beyond the confirmed focus</h2><section id="wider">', 1)
base = base.replace('<section id="questions">', '<h2 class="part-head">Exam practice · reveal, edit and run</h2><section id="questions">', 1)
base = base.replace('<section id="corrections">', '''<section id="recap"><h2>Quick revision / last 15 minutes</h2><div class="grid"><div class="tile"><b>OOP in one glance</b><p>class blueprint → object instance → constructor initializes → public functions access private data → destructor cleans up. :: defines functions outside class. Inheritance reuses a base class.</p></div><div class="tile"><b>SQL in one glance</b><p>CREATE / ALTER / DROP = structure. INSERT / UPDATE / DELETE = data. SELECT columns FROM table WHERE row condition GROUP BY group HAVING group condition ORDER BY sorting.</p></div><div class="tile"><b>Network in one glance</b><p>LAN: building. MAN: city. WAN: wide area. Star: central switch; bus: shared backbone. Repeater regenerates; router connects networks.</p></div><div class="tile"><b>Check before submitting</b><p>Turbo C (.C) for procedural code; Turbo C++ (.CPP) for classes. Semicolons, braces, correct header, valid return type, input, and sample output. Never claim these questions are guaranteed.</p></div></div><p><button id="resetProgress" type="button">Reset study progress</button> <span id="studyProgress" class="small" aria-live="polite"></span></p></section><section id="corrections">''', 1)
base = base.replace('<a href="#sources">Sources</a></nav>', '<a href="#recap">Quick revision</a><a href="#sources">Sources</a></nav>', 1)
# Add clickable practice panes to every C / C++ code answer, including linked code questions.
count = [0]
def add_lab(m):
    raw = m.group(1)
    if not raw.startswith('#include'):
        return m.group(0)
    count[0] += 1
    lang = 'cpp' if 'iostream.h' in raw or 'fstream.h' in raw else 'c'
    return m.group(0) + '<div class="lab-link"><button type="button" class="open-lab" data-code="' + str(count[0]) + '" data-lang="' + lang + '">✎ Open practice window · ' + ('.CPP' if lang == 'cpp' else '.C') + '</button><span class="small">Edit the answer and try an input</span></div>'
base = re.sub(r'<pre><code>(.*?)</code></pre>', add_lab, base, flags=re.S)
base = base.replace('<a href="#oop">Item class program</a>', '<a href="#oop" class="practice-jump" data-match="class Item">Item class program</a>')
base = base.replace('<a href="#cprograms">linear-search .C program</a>', '<a href="#cprograms" class="practice-jump" data-match="int a[5]">linear-search .C program</a>')
base = base.replace('<a href="#oop" class="practice-jump" data-match="class Item">Item class program</a>', '<a href="#oop" class="practice-jump" data-match="class Item">Open the Item answer in the practice window</a>')
base = base.replace('<a href="#cprograms" class="practice-jump" data-match="int a[5]">linear-search .C program</a>', '<a href="#cprograms" class="practice-jump" data-match="int a[5]">Open the linear-search answer in the practice window</a>')
base = base.replace('<li><strong>Bandwidth:</strong> a communication channel’s capacity to carry data, commonly expressed in bits per second.</li>', '<li><strong>Bandwidth:</strong> the range of frequencies a channel can carry, measured in Hz; in casual networking usage, the term also describes data capacity, measured in bps. The two measurements are not identical.</li>')
base = base.replace('FOREIGN KEY</strong> links to a candidate/primary key in another table;', 'FOREIGN KEY</strong> references a primary or unique key in another table;')
base = base.replace('foreign key</b> in BOOK points to a key in PUBLISHER.', 'foreign key</b> in BOOK points to a primary or unique key in PUBLISHER.')
base = base.replace('</body>', '''<div class="modal" id="lab" hidden role="dialog" aria-modal="true" aria-labelledby="labTitle"><div class="modal-panel"><div class="modal-top"><div><strong id="labTitle">Practice lab</strong><p id="labType" class="small"></p></div><button type="button" id="closeLab" aria-label="Close practice window">✕ Close</button></div><p class="small" id="labNotice">Run submits the code and input to a public Judge0 sandbox. It runs GCC C / C++, <strong>not the actual Turbo compiler</strong>; old Turbo C++ headers are adapted for execution. File programs use a temporary sandbox and may not work here. Don’t enter private data.</p><div class="editor-grid"><div><label for="editor"><strong>Editable answer</strong></label><textarea id="editor" spellcheck="false" aria-label="Edit program code"></textarea></div><div><label for="stdin"><strong>Input (stdin)</strong></label><textarea id="stdin" placeholder="e.g. 7" aria-label="Program input"></textarea><button type="button" id="runCode" class="run">▶ Compile &amp; run</button><button type="button" id="resetCode">Restore answer</button><h3>Output / errors</h3><pre id="runOutput" role="status" aria-live="polite">Ready to run.</pre></div></div></div></div><script src="app.js" defer></script></body>''')
base = base.replace('</style>', '''.part-head{margin:42px 0 14px;font-size:18px;letter-spacing:-.02em;color:#7e5d2f;text-transform:uppercase}.lab-link{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:12px 0}.open-lab,.run{background:#075db0;color:white;border:1px solid #075db0;padding:9px 13px}.open-lab:hover,.run:hover{background:#074c8e}.modal[hidden]{display:none}.modal{position:fixed;inset:0;background:rgba(13,18,25,.66);display:flex;align-items:center;justify-content:center;z-index:20;padding:12px}.modal-panel{background:#fff;border-radius:12px;width:min(1080px,100%);max-height:95vh;overflow:auto;padding:18px;box-shadow:0 24px 70px #0005}.modal-top{display:flex;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line);padding-bottom:10px}.modal-top p{margin:2px 0}.editor-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:16px}.editor-grid textarea{width:100%;border:1px solid #ccc;border-radius:6px;font:13px/1.5 ui-monospace,Consolas,monospace;padding:10px;background:#fafafa;color:#181818;resize:vertical}#editor{height: min(59vh,590px);min-height:260px;tab-size:4}#stdin{height:90px}#runOutput{min-height:140px;max-height:230px;white-space:pre-wrap;overflow:auto;word-break:break-word}.editor-grid button{margin:8px 7px 0 0}.editor-grid h3{margin:17px 0 4px}@media(max-width:700px){.editor-grid{grid-template-columns:1fr}.modal-panel{padding:12px}#editor{height:38vh;min-height:190px}.modal{align-items:stretch}.modal-panel{max-height:100%}}@media print{.modal,.lab-link,.nav,#resetProgress{display:none!important}details .answer{display:block!important}} </style>''')
(ROOT / 'index.html').write_text(base, encoding='utf-8')
print('built', len(base), 'characters;', base.count('<section '), 'sections;', base.count('class="open-lab"'), 'C/C++ practice panes')
