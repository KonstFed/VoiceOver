import React from "react";
import styles from './Header.module.scss'

const Header = () => {
    return (
        <div className={styles.header}>
            <div className={styles.menu}>
                <a className={styles.menu_item} href="/text-to-speech">Text to Speech</a>
                <a className={styles.menu_item} href="/speech-to-speech">Speech to Speech</a>
            </div>
        </div>
    )
}

export default Header