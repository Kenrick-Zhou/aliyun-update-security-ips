# aliyun-update-security-ips

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/Kenrick-Zhou/aliyun-update-security-ips?style=social)](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Kenrick-Zhou/aliyun-update-security-ips?style=social)](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/Kenrick-Zhou/aliyun-update-security-ips)](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/issues)

[中文文档](README.md) | English

</div>

Automatically update Alibaba Cloud RDS & Tair(Redis) security IP whitelist

Perfect for DDNS environments and remote access scenarios, balancing security and convenience.

_Supports automatic whitelist updates for Alibaba Cloud RDS and Tair (Redis) instances.
Contributions welcome!_

## ✨ Features

- 🔄 Automatic periodic security IP whitelist updates
- 🎯 Support for both RDS and Tair(Redis) instances
- 📱 Multiple notification methods (Bark, PushDeer)
- ⚡ Perfect for DDNS environments
- 🛡️ Secure and convenient access management
- 📝 Detailed logging

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Alibaba Cloud AccessKey with RDS/Tair permissions
- RDS or Tair instances

### Installation

```bash
# Clone the repository
git clone https://github.com/Kenrick-Zhou/aliyun-update-security-ips.git
cd aliyun-update-security-ips

# Quick setup (recommended)
./install.sh

# Or manual setup
make setup
make install
```

### Configuration

1. **Configure Alibaba Cloud Credentials**
   ```bash
   cp .env.example .env
   # Edit .env and add your AccessKey
   ```

2. **Configure Instances**
   ```bash
   cp config.example.yml config.yml
   # Edit config.yml and configure your RDS/Tair instances
   ```

3. **Test**
   ```bash
   # Manual run (once)
   python update.py
   
   # Or use Makefile
   make run-manual
   ```

### Usage

#### Manual Mode (One-time)
For temporary access needs:
```bash
python update.py
```

#### Daemon Mode (Recommended)
For servers in DDNS environments:
```bash
# Method 1: Using nohup
nohup python updated.py > nohup.out 2>&1 &

# Method 2: Using Makefile
make run-daemon
make check-daemon  # Check status
make stop-daemon   # Stop daemon
```

#### System Service (Production)
See [README.md](README.md) for systemd/launchd configuration.

## 📋 Documentation

- [Contributing Guide](CONTRIBUTING.md)
- [FAQ](FAQ.md)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)
- [Security Policy](SECURITY.md)

## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guide](CONTRIBUTING.md).

We welcome:
- 🐛 Bug reports
- 💡 Feature requests
- 📝 Documentation improvements
- 💻 Code contributions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Kenrick-Zhou/aliyun-update-security-ips&type=Date)](https://star-history.com/#Kenrick-Zhou/aliyun-update-security-ips&Date)

## 🙏 Acknowledgments

- Thanks to Alibaba Cloud for their SDK
- Thanks to all contributors
- Thanks to all users and supporters

---

<div align="center">

**If you find this project helpful, please give it a ⭐ Star!**

Made with ❤️ by [Kenrick-Zhou](https://github.com/Kenrick-Zhou)

</div>
