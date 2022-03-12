# Maintainer: Ruslan Sergin <ruslan.sergin@gmail.com>
#             Stevan Antoine (temporary)
pkgname=arcolinux-logout
pkgver=22.03_12
pkgrel=2
pkgdesc="Beautiflul ArcoLinux logout screen"
url="https://github.com/a2n-s/arcolinux-logout"
arch=('x86_64')
depends=('python3' 'python-cairo')
license=('GPL3')
source=("$pkgname-$pkgver.tar.gz::https://github.com/a2n-s/arcolinux-logout/archive/refs/tags/${pkgver//_/-}.tar.gz#branch=lock/other")
# md5sums=('23d72b9ccd59689b4c47c07b416a7344')
md5sums=('SKIP')

package () {
    mkdir -p "${pkgdir}" 
    mv "${srcdir}/${pkgname}-${pkgver//_/-}/"{usr,etc} "${pkgdir}/"
    mv "${srcdir}/${pkgname}-${pkgver//_/-}/LICENSE" "${pkgdir}/usr/share/arcologout"
    mv "${srcdir}/${pkgname}-${pkgver//_/-}/README.md" "${pkgdir}/usr/share/arcologout"
}
