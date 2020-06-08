import React from 'react';

export function Footer() {
    return (
        <footer className="mod-footer">
            <div className="container footer-container">
                <div className="footer-content">
                    <div className="footer-info-left">
                        <div className="logo">
                            <img src="http://kaartgroup.com/wp-content/uploads/2019/09/Kaart-Final-Logo_Horizontal.png" alt="" class="img-responsive" />
                        </div>
                        <div className="social-networks">
                            <ul>
                                <li>
                                    <a href="https://www.facebook.com/kaartgroup/">
                                        <img src="http://kaartgroup.com/wp-content/uploads/2018/12/KG-Facebook-icon.svg" alt="KG-Facebook-icon" height="18" />
                                    </a>
                                </li>
                                <li>
                                    <a href="https://github.com/KaartGroup">
                                        <img src="http://kaartgroup.com/wp-content/uploads/2018/12/KG-GitHub-Icon.svg" alt="KG-GitHub-Icon" height="18" />
                                    </a>
                                </li>
                                <li>
                                    <a href="https://wiki.openstreetmap.org/wiki/Kaart">
                                        <img src="http://kaartgroup.com/wp-content/uploads/2018/12/KG-WIKI-icon.svg" alt="KG-WIKI-icon" height="18" />
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div className="footer-info-right">
                        <a href="https://www.google.com/maps/search/?api=1&amp;query= 750 Main Street, Suite 200 <br>Grand Junction, CO 81501" target="_blank" rel="noopener noreferrer" className="footer-info-address">
                            <div>750 Main Street, Suite 200 <br />Grand Junction, CO 81501</div>
                        </a>
                    </div>
                </div>
                <p className="footer-info-copy-right">© 2020 Kaart Group LLC. All rights reserved.</p>
            </div>
        </footer>
    );
}