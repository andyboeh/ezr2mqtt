pkgname=ezr2mqtt-git
pkgver=r9.b85d0b2
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
        'ezr2mqtt.service')
provides=('ezr2mqtt')
conflicts=('ezr2mqtt')
sha256sums=('SKIP'
            '5aa2d0f64b931631332384a59db877757ab44d9a16412476d135e29e09c4e640'
            '1b289feebb0b594fd82a52fdfa213e82a42295dba1b3dc92602bd42e6d2ee5f6'
            'd5edf14bad7d50e692dc58e5525056482e40c8afecd5cf2083ecb87fb92a4daf')
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
  install -Dm644 ezr2mqtt.yaml "${pkgdir}/opt/ezr2mqtt/ezr2mqtt.yaml"
}
