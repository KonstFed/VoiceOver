import React from "react";
import styles from "./TextToSpeech.module.scss"
import photo1 from '../../images/photo1.png'
import download from '../../images/download.svg'
import sound from '../../images/sound.svg'
import cn from "classnames"

const TextToSpeech = () => {
    return (
        <div className={styles.block}>
            <div className={styles.inner_block}>
                <div className={styles.left_part}>
                    <div className={styles.left_part_up}>
                        <div className={styles.title}>
                            Write your text here
                        </div>
                        <div className={styles.input}>
                            <textarea className={styles.textarea} name="" id="1" cols="30" rows="10" />
                        </div>
                    </div>
                    <div className={styles.left_part_down}>
                        <div className={styles.left_part_down_text}>
                        You write the text, and then it transforms into the speech of the 
                        chosen voice. You can <span>download</span> and <span>play</span> the speech.
                        </div>
                    </div>
                </div>
                <div className={styles.right_part}>
                    <div className={styles.left_part_up}>
                        <div className={styles.title}>
                            Choose your voice
                        </div>
                        <div className={styles.cards}>
                            <div className={styles.card}>
                                <img className={styles.card_image} src={photo1} alt="" />
                                <div className={styles.card_name}>
                                    Anni <br /> Edmona
                                </div>
                            </div>
                            <div className={styles.card}>
                                <img className={styles.card_image} src={photo1} alt="" />
                                <div className={styles.card_name}>
                                    Anni <br /> Edmona
                                </div>
                            </div>
                            <div className={styles.card}>
                                <img className={styles.card_image} src={photo1} alt="" />
                                <div className={styles.card_name}>
                                    Anni <br /> Edmona
                                </div>
                            </div>
                            <div className={styles.card}>
                                <img className={styles.card_image} src={photo1} alt="" />
                                <div className={styles.card_name}>
                                    Anni <br /> Edmona
                                </div>
                            </div>
                            <div className={styles.card}>
                                <img className={styles.card_image} src={photo1} alt="" />
                                <div className={styles.card_name}>
                                    Anni <br /> Edmona
                                </div>
                            </div>
                            <div className={styles.card}>
                                <img className={styles.card_image} src={photo1} alt="" />
                                <div className={styles.card_name}>
                                    Anni <br /> Edmona
                                </div>
                            </div>

                        </div>
                    </div>
                    <div className={styles.right_part_down}>
                        <div className={styles.buttons}>
                            <button className={styles.button} type="button">
                                <img src={sound} alt="" />
                            </button>
                            <button className={cn(styles.button, styles.action)} type="button">
                                <img src={download} alt="" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default TextToSpeech;