# SecureAuthX 🔐

SecureAuthX is a Django-based smart authentication system that enhances user login security using OTP (One-Time Password) verification.  
It adds an extra layer of protection beyond traditional username-password authentication.

---

## 📌 Project Overview

This project implements a secure authentication workflow where users must verify their identity using an OTP sent via email before gaining access.  
The goal is to demonstrate secure session handling and multi-step authentication using Django.

---

## 🚀 Features

- User Registration & Login
- OTP-Based Authentication
- Email OTP Verification
- Secure Session Management
- Time-based OTP Expiration
- Basic Security Validation

---

## 🛠 Tech Stack

- Python
- Django
- SQLite (Default)
- HTML / CSS
- SMTP (for OTP email delivery)

---

## 🔐 How It Works

1. User logs in using username & password.
2. System generates a One-Time Password (OTP).
3. OTP is sent to the registered email address.
4. User enters OTP for verification.
5. If OTP is valid and not expired → Login Successful.

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository
