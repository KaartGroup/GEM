import React from "react";

export function Header() {
  return (
    <header className="mod-nav">
      <div className="container nav-container">
        <div className="logo">
          <a className="logo-link" href="http://kaartgroup.com">
            <img
              className="img-responsive"
              src="/static/react/res/Kaart Final Logo_Circle.svg"
              alt=""
            />
          </a>
        </div>
        <div className="title"> GEM </div>
      </div>
    </header>
  );
}
