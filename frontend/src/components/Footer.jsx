function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-content">
        <p className="footer-text">
          © {currentYear} Find Your AI Model. All rights reserved.
        </p>
        <p className="footer-disclaimer">
          We may earn commissions from links on this site.
        </p>
      </div>
    </footer>
  );
}

export default Footer;
