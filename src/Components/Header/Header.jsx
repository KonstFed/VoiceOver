import React from "react";
import styles from './Header.module.css'

const Header = () => {
    return (
        <div className={styles.header}>
            <div className={styles.menu}>
                <a className={styles.menu_item} href="#">Text to Speech</a>
                <a className={styles.menu_item} href="#">Speech to Speech</a>
            </div>
        </div>
    )
}

export default Header