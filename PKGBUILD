# Maintainer: Ruslan Sergin <ruslan.sergin@gmail.com>
#             Stevan Antoine (temporary)
pkgname=arcolinux-logout-a2n-s-git
pkgver=22.03_12
pkgrel=2
pkgdesc="Beautiflul ArcoLinux logout screen"
url="https://github.com/a2n-s/arcolinux-logout.git"
arch=('x86_64')
depends=('python3' 'python-cairo')
provides=(arcolinux-logout)
conflicts=(arcolinux-logout)
license=('GPL3')
source=("git+$url#branch=lock/other")
# md5sums=('23d72b9ccd59689b4c47c07b416a7344')
md5sums=('SKIP')

package () {
    cd arcolinux-logout
    mkdir -p "${pkgdir}" 
    mv {usr,etc} "${pkgdir}/"
    mv LICENSE "${pkgdir}/usr/share/arcologout"
    mv README.md "${pkgdir}/usr/share/arcologout"
}
