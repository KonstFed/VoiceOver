import React from "react";
import styles from './SpeechToSpeech.module.scss'
import photo1 from '../../images/photo1.png'
import sound from '../../images/sound.svg'
import download from '../../images/download.svg'
import record from '../../images/record.svg'
import cn from "classnames"


const SpeechToSpeech = () => {
    return (
        <div className={styles.block}>
            <div className={styles.inner_block}>
                <div className={styles.left_part}>
                    <div className={styles.left_part_up}>
                        <div className={styles.title}>
                            Record your voice
                        </div>
                        <div className={styles.record_block}>
                            <button className={styles.record_button} type="button">
                                <img className={styles.record_button_image} src={record} alt="" />
                            </button>
                        </div>
                    </div>
                    <div className={styles.left_part_down}>
                        You <span>record</span> your speech by clicking the button above, then it transforms 
                        into the chosen voice. You can <span>download</span> and <span>play</span> it.
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

export default SpeechToSpeech;