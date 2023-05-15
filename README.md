# pdf-password
PDF 文件的加密与去密

在 PDF 文件的安全设置中，有两种类型的密码：用户密码（user password）和所有者密码（owner password）。

* 用户密码（user password）：也称为打开密码（open password），它用于限制对 PDF 文件的访问。当一个 PDF 文件被设置了用户密码时，在尝试打开文件时，需要提供正确的用户密码才能成功打开和查看文件内容。

* 所有者密码（owner password）：也称为权限密码（permissions password），它用于控制对 PDF 文件的权限和操作。拥有正确的所有者密码可以获得更高的权限，例如打印、复制、编辑或更改 PDF 文件的内容等。

PDF 的加密和所有者密码去密都可以通过 PyPDF2 库来实现，而用户密码则需要利用 pikepdf 暴力破解或字典破解。

这里使用了 zxcvbn001 的口令爆破字典，有键盘组合字典、拼音字典、字母与数字混合这三种类型。

https://github.com/zxcvbn001/password_brute_dictionary

