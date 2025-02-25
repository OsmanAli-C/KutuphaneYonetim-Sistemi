
Bu proje, bir kütüphane yönetim sistemi geliştirme amacıyla hazırlanmıştır. Kullanıcılar ve admin için farklı yetkiler ve arayüzler sunmaktadır. Sistem, MongoDB veri tabanını kullanarak işlemleri yönetir.

-Kullanıcı olarak sisteme giriş yapmak için önce kayıt olunması gerekmektedir.

-Geçerli bir e-posta adresi ile kayıt olunması durumunda bilgilendirme e-postaları gönderilmektedir, geçerli bir e-posta adresi ile kayıt olunmaması durumunda bilgilendirme e-postaları gönderilmemektedir geri kalan özellikler tam fonksiyon kullanılabilmektedir

-Kullanıcı ile admin farklı arayüzlere sahiptir farklı yetkileri vardır

-Veri Tabanı olarak MongoDB kullanılmıştır

-Admin olarak giriş yapıldığında kitap ekleme, kitap silme, kullancı yasaklama, ödünç istenen kitapları ödünç verme veya isteği reddetme yetkileri vardır

-kullanıcı olarak giriş yapıldığında kitap isteme, kitap ödünç alma, kitap isteğini iptal etme, kitap iade etme, şifre değiştirme yetkileri vardır

-Projede kullanılan kütüphaneler ve sürümleri requirements.txt dosyasındadır

-Bu proje, gizli bilgilerin güvenli bir şekilde saklanması için bir `.env` dosyasına ihtiyaç duyar. Projeyi çalıştırmadan önce aşağıdaki adımları izleyerek `.env` dosyasını oluşturun:

-Proje klasöründe bir `.env` dosyası oluşturun ve içine aşağıdaki bilgileri girin:

```plaintext
EMAIL=<E-postanızı buraya yazın>
PASSWORD=<E-posta şifrenizi buraya yazın>
MONGO_URI=<MongoDB bağlantı URL'nizi buraya yazın>
ADMİN_PASSWORD=<Admin girişi için şifre>
