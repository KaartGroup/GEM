import React from 'react';

export function Banner() {
   

    return (
        <section className="banner">
            <img className="img-responsive img-banner opacity" src="http://via.placeholder.com/1400x700" alt="" />
            <div className="banner-layer-img" style={{ background: "url('https://images.pexels.com/photos/41949/earth-earth-at-night-night-lights-41949.jpeg') center center / cover no-repeat" }}></div>   
            <div className="banner-container">
                <div className="divider"></div>
                <div className="button-container" style={{ display: "center-block" }}>
                    <a href="/editor"><button className='loginbtn'> Try GEM</button></a>           
                </div>
            </div>   
        </section>
    );
}