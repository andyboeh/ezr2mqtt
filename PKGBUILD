pkgname=ezr2mqtt-git
pkgver=r8.fe7be27
pkgrel=1
pkgdesc="Simple Möhlenhoff Alpha 2 (EZR) to MQTT bridge"
arch=('any')
url="https://github.com/andyboeh/ezr2mqtt"
license=('GPL')
depends=('python' 'python-paho-mqtt' 'python-requests')
install='ezr2mqtt.install'
source=('ezr2mqtt-git::git+https://github.com/andyboeh/ezr2mqtt.git'
        'ezr2mqtt.install'
        'ezr2mqtt.sysusers'
        'ezr2mqtt.service'
        'ezr2mqtt.yaml')
provides=('ezr2mqtt')
conflicts=('ezr2mqtt')
sha256sums=('SKIP' 
            'SKIP'
            'SKIP'
            'SKIP'
            'SKIP')
backup=('opt/ezr2mqtt/ezr2mqtt.yaml')

pkgver() {
  cd "$pkgname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
  cd "${pkgname}"
  install -d "${pkgdir}/opt/ezr2mqtt"
  cp ezr2mqtt.py "${pkgdir}/opt/ezr2mqtt/ezr2mqtt.py"
  cp -R pyezr "${pkgdir}/opt/ezr2mqtt/"
  install -Dm644 "${srcdir}/ezr2mqtt.service" "${pkgdir}/usr/lib/systemd/system/ezr2mqtt.service"
  install -Dm644 "${srcdir}/ezr2mqtt.sysusers" "${pkgdir}/usr/lib/sysusers.d/ezr2mqtt.conf"
  install -Dm644 "${srcdir}/ezr2mqtt.yaml" "${pkgdir}/opt/ezr2mqtt/ezr2mqtt.yaml"
}
