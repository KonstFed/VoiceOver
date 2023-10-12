import React from "react";
import styles from './Header.module.scss'
import { useLocation } from "react-router-dom";

const Header = () => {
    const location = useLocation();
    const isTextToSpeechActive = location.pathname === '/text-to-speech';
    const isSpeechToSpeechActive = location.pathname === '/speech-to-speech';

    return (
        <div className={styles.header}>
            <div className={styles.menu}>
                <a className={`${styles.menu_item} ${isTextToSpeechActive ? styles.active : ''}`} href="/text-to-speech">Text to Speech</a>
                <a className={`${styles.menu_item} ${isSpeechToSpeechActive ? styles.active : ''}`} href="/speech-to-speech">Speech to Speech</a>
            </div>
        </div>
    )
}

export default Header;
