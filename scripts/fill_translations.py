#!/usr/bin/env python3
"""Fill en/ru translations in django.po files."""
from pathlib import Path

import polib

BASE = Path(__file__).resolve().parent.parent / 'locale'

TRANSLATIONS = {
    'en': {
        'Blog o masáži a relaxaci Praha | Black Velvet': 'Massage & Relaxation Blog Prague | Black Velvet',
        'Tipy, rady a články o masáži, relaxaci a wellness v Praze. Praktické informace od odborníků Black Velvet Spa.': (
            'Tips, advice and articles about massage, relaxation and wellness in Prague. '
            'Practical information from Black Velvet Spa experts.'
        ),
        'Blog': 'Blog',
        'Domů': 'Home',
        'Masáž a relaxace Praha — Luxusní spa salon | Black Velvet': (
            'Massage & Relaxation Prague — Luxury Spa Salon | Black Velvet'
        ),
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy. Aromaterapeutické, relaxační a sportovní masáže. Rezervujte online.': (
            'Black Velvet Spa — a luxury massage salon in the heart of Prague. '
            'Aromatherapy, relaxation and sports massages. Book online.'
        ),
        'Vaše jméno': 'Your name',
        'Email': 'Email',
        'Telefon': 'Phone',
        'Vaše zpráva': 'Your message',
        'Ceník masáží Praha — Ceny a délky | Black Velvet': 'Massage Price List Prague — Prices & Duration | Black Velvet',
        'Kompletní ceník masáží v Black Velvet Spa Praha. Transparentní ceny aromaterapeutické, sportovní a relaxační masáže.': (
            'Complete massage price list at Black Velvet Spa Prague. '
            'Transparent prices for aromatherapy, sports and relaxation massages.'
        ),
        'Ceník': 'Price list',
        'Kontakt — Black Velvet Spa Vinohrady, Praha 2': 'Contact — Black Velvet Spa Vinohrady, Prague 2',
        'Kontaktujte Black Velvet Spa ve Vinohradech, Praha 2. Adresa Lužická 1416/29, telefon, email a kontaktní formulář. Rezervace masáže online nebo telefonicky.': (
            'Contact Black Velvet Spa in Vinohrady, Prague 2. Address Lužická 1416/29, phone, email and contact form. '
            'Book a massage online or by phone.'
        ),
        'Kontakt': 'Contact',
        'Zpráva byla odeslána. Brzy se vám ozveme.': 'Your message has been sent. We will get back to you soon.',
        'Rozvrh masérek Praha — Otevírací doba | Black Velvet': 'Masseuse Schedule Prague — Opening Hours | Black Velvet',
        'Rozvrh masérek a otevírací doba Black Velvet Spa ve Vinohradech, Praha 2. Aktuální směny a volné termíny pro rezervaci masáže.': (
            'Masseuse schedule and opening hours of Black Velvet Spa in Vinohrady, Prague 2. '
            'Current shifts and available slots for massage booking.'
        ),
        'Rozvrh': 'Schedule',
        'O nás — Luxusní masážní salon Praha | Black Velvet': 'About Us — Luxury Massage Salon Prague | Black Velvet',
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy 1. Profesionální masérky, klidné prostředí a individuální péče.': (
            'Black Velvet Spa — a luxury massage salon in the heart of Prague 1. '
            'Professional masseuses, calm atmosphere and individual care.'
        ),
        'O nás': 'About us',
        'Pravidla salonu | Black Velvet Spa Praha': 'Salon Rules | Black Velvet Spa Prague',
        'Pravidla a zásady návštěvy Black Velvet Spa. Rezervace, zrušení termínu, hygiena a chování v salonu.': (
            'Rules and guidelines for visiting Black Velvet Spa. '
            'Booking, cancellation, hygiene and salon conduct.'
        ),
        'Pravidla salonu': 'Salon rules',
        'Zásady ochrany osobních údajů | Black Velvet': 'Privacy Policy | Black Velvet',
        'Zásady ochrany osobních údajů Black Velvet Spa. Informace o zpracování dat a vašich právech.': (
            'Privacy policy of Black Velvet Spa. Information about data processing and your rights.'
        ),
        'Zásady ochrany': 'Privacy policy',
        'Vyberte masáž': 'Choose a massage',
        'Vyberte masérku': 'Choose a masseuse',
        'Libovolná masérka': 'Any masseuse',
        'Datum': 'Date',
        'Čas': 'Time',
        'Datum musí být v budoucnosti.': 'The date must be in the future.',
        'Jméno a příjmení': 'Full name',
        'Poznámka (volitelné)': 'Note (optional)',
        'Rezervace masáže Praha — Online booking | Black Velvet': 'Massage Booking Prague — Online Booking | Black Velvet',
        'Rezervujte masáž online v Black Velvet Spa Praha. Vyberte službu, masérku, termín a potvrďte rezervaci.': (
            'Book a massage online at Black Velvet Spa Prague. '
            'Choose a service, masseuse, time slot and confirm your booking.'
        ),
        'Rezervace': 'Booking',
        'Služba': 'Service',
        'Masérka': 'Masseuse',
        'Termín': 'Appointment',
        'Potvrzení': 'Confirmation',
        'Tento termín je již obsazený. Vyberte prosím jiný.': 'This time slot is already taken. Please choose another one.',
        'Potvrzení rezervace — Black Velvet Spa': 'Booking Confirmation — Black Velvet Spa',
        'Dobrý den {name},\n\nVaše rezervace byla potvrzena.\nSlužba: {service}\nTermín: {date} {time}\n\nPotvrzení: {url}': (
            'Hello {name},\n\nYour booking has been confirmed.\nService: {service}\n'
            'Appointment: {date} {time}\n\nConfirmation: {url}'
        ),
        'Relaxační a terapeutické masáže Praha | Black Velvet': 'Relaxation & Therapeutic Massages Prague | Black Velvet',
        'Kompletní nabídka masáží v Praze — aromaterapeutická, klasická, sportovní, relaxační a lymfatická. Rezervujte termín online.': (
            'Full range of massages in Prague — aromatherapy, classic, sports, '
            'relaxation and lymphatic. Book online.'
        ),
        'Masáže': 'Massages',
        'Naše masérky Praha — Odbornice Black Velvet Spa': 'Our Masseuses Prague — Black Velvet Spa Experts',
        'Seznamte se s našimi certifikovanými masérkami v Praze. Aromaterapie, sportovní a relaxační masáže od profesionálek.': (
            'Meet our certified masseuses in Prague. Aromatherapy, sports and relaxation '
            'massages from professionals.'
        ),
        'Masérky': 'Masseuses',
        'Související články': 'Related articles',
        'Tipy a rady o masáži a relaxaci': 'Tips and advice about massage and relaxation',
        'Zatím žádné články.': 'No articles yet.',
        'Stránkování': 'Pagination',
        'Stránka nenalezena.': 'Page not found.',
        'Zpět na hlavní stranu': 'Back to homepage',
        'Došlo k chybě serveru. Zkuste to prosím později.': 'A server error occurred. Please try again later.',
        'Masáž a relaxace Praha': 'Massage & Relaxation Prague',
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy. Odhalte svůj vlastní ráj.': (
            'Black Velvet Spa — a luxury massage salon in the heart of Prague. Discover your own paradise.'
        ),
        'Rezervovat': 'Book now',
        'Naše masáže': 'Our massages',
        'Masáže pro tělo i duši': 'Massages for body and soul',
        'Všechny masáže': 'All massages',
        'Odbornice pro váš komfort a relaxaci': 'Experts for your comfort and relaxation',
        'Všechny masérky': 'All masseuses',
        'Čtyři kroky k dokonalé relaxaci': 'Four steps to perfect relaxation',
        'Prohlédněte si nabídku a vyberte masáž, která vám nejvíce vyhovuje.': (
            'Browse our offer and choose the massage that suits you best.'
        ),
        'Rezervujte termín': 'Book an appointment',
        'Online přes náš systém nebo telefonicky — rychle a jednoduše.': (
            'Online through our system or by phone — quick and easy.'
        ),
        'Přijďte a relaxujte': 'Come and relax',
        'Uvítáme vás v salonu a připravíme vše pro dokonalý zážitek.': (
            'We will welcome you at the salon and prepare everything for a perfect experience.'
        ),
        'Odejděte odpočatí': 'Leave refreshed',
        'Odnesete si hluboký klid a regeneraci pro tělo i mysl.': (
            'You will take away deep calm and regeneration for body and mind.'
        ),
        'Co říkají naši klienti': 'What our clients say',
        'Zobrazit kontakt a mapu': 'Show contact and map',
        'Kontakt a mapa': 'Contact & map',
        'Najdete nás v srdci Prahy': 'Find us in the heart of Prague',
        'Otevírací doba': 'Opening hours',
        'Denně od 9:00 do 5:00 ráno': 'Daily from 9 AM to 5 AM',
        'Odhalte svůj vlastní ráj': 'Discover your own paradise',
        'Rezervovat masáž': 'Book a massage',
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy, kde se setkává profesionalita s klidem a diskrétní atmosférou.': (
            'Black Velvet Spa — a luxury massage salon in the heart of Prague, '
            'where professionalism meets calm and a discreet atmosphere.'
        ),
        'Náš příběh': 'Our story',
        'Vytvořili jsme prostor, kde se můžete plně uvolnit a na chvíli zapomenout na každodenní shon. Každá masáž je vedena zkušenými masérkami, které dbají na vaše individuální potřeby a komfort.': (
            'We created a space where you can fully unwind and forget the daily rush for a while. '
            'Every massage is performed by experienced masseuses who care about your individual needs and comfort.'
        ),
        'Co nás odlišuje': 'What sets us apart',
        'Profesionální tým certifikovaných masérek': 'Professional team of certified masseuses',
        'Klidné a diskrétní prostředí v centru Prahy 1': 'Calm and discreet environment in the centre of Prague 1',
        'Široká nabídka relaxačních a terapeutických masáží': 'Wide range of relaxation and therapeutic massages',
        'Jednoduchá online rezervace termínů': 'Easy online appointment booking',
        'Naše hodnoty': 'Our values',
        'Respekt, diskrétnost a péče o detail jsou pro nás základem každé návštěvy. Věříme, že kvalitní masáž obnovuje tělo i mysl — a proto klademe důraz na osobní přístup ke každému klientovi.': (
            'Respect, discretion and attention to detail are the foundation of every visit. '
            'We believe a quality massage restores body and mind — which is why we focus on a personal approach to every client.'
        ),
        'Kontaktujte nás': 'Contact us',
        'Máte dotaz nebo chcete rezervovat termín? Jsme tu pro vás.': (
            'Have a question or want to book an appointment? We are here for you.'
        ),
        'Rychlý kontakt': 'Quick contact',
        'Adresa': 'Address',
        'Kde nás najdete': 'Where to find us',
        'Mapa — Black Velvet Spa Praha': 'Map — Black Velvet Spa Prague',
        'Otevřít v Mapách': 'Open in Maps',
        'Zkontrolujte prosím vyplněná pole.': 'Please check the filled fields.',
        'Odeslat zprávu': 'Send message',
        'Zpráva odeslána': 'Message sent',
        'Děkujeme. Brzy se vám ozveme.': 'Thank you. We will get back to you soon.',
        'Ceník masáží Praha': 'Massage Price List Prague',
        'Transparentní ceny všech masáží v Black Velvet Spa. Všechny ceny jsou uvedeny včetně DPH.': (
            'Transparent prices for all massages at Black Velvet Spa. All prices include VAT.'
        ),
        'Ceník podle délky masáže': 'Price list by massage duration',
        'Délka masáže': 'Massage duration',
        'min': 'min',
        'Ceník bude brzy k dispozici.': 'The price list will be available soon.',
        'Zásady ochrany osobních údajů': 'Privacy policy',
        'Black Velvet Spa zpracovává osobní údaje v souladu s nařízením GDPR a platnými právními předpisy České republiky.': (
            'Black Velvet Spa processes personal data in accordance with GDPR '
            'and applicable laws of the Czech Republic.'
        ),
        'Správce údajů': 'Data controller',
        'Účel zpracování': 'Purpose of processing',
        'Osobní údaje zpracováváme za účelem rezervace masáží, komunikace s klienty a plnění smluvních povinností.': (
            'We process personal data for massage bookings, client communication '
            'and fulfilment of contractual obligations.'
        ),
        'Vaše práva': 'Your rights',
        'Máte právo na přístup, opravu, výmaz a přenositelnost údajů. Kontaktujte nás na': (
            'You have the right to access, rectify, erase and port your data. Contact us at'
        ),
        'Aby byl váš zážitek co nejpříjemnější pro vás i ostatní klienty, prosíme o dodržování následujících zásad.': (
            'To make your experience as pleasant as possible for you and other clients, '
            'please follow these guidelines.'
        ),
        'Rezervace a dochvilnost': 'Booking and punctuality',
        'Termín rezervujte předem online nebo telefonicky. Doporučujeme dorazit 5–10 minut před začátkem masáže. Při zpoždění může být délka masáže zkrácena bez snížení ceny.': (
            'Book your appointment in advance online or by phone. We recommend arriving 5–10 minutes '
            'before the massage starts. In case of delay, the massage duration may be shortened without a price reduction.'
        ),
        'Zrušení termínu': 'Cancellation',
        'Rezervaci zrušte nejpozději 24 hodin předem telefonicky nebo e-mailem. Při pozdním zrušení nebo nedostavení se si vyhrazujeme právo účtovat storno poplatek.': (
            'Cancel your booking at least 24 hours in advance by phone or email. '
            'For late cancellation or no-show, we reserve the right to charge a cancellation fee.'
        ),
        'Hygiena a zdraví': 'Hygiene and health',
        'Před masáží se prosím osprchujte. Při akutních infekcích, horečce nebo kožních onemocněních masáž odložte. Informujte masérku o alergiích, zraněních nebo zdravotních omezeních.': (
            'Please shower before the massage. Postpone the massage if you have acute infections, '
            'fever or skin conditions. Inform the masseuse about allergies, injuries or health restrictions.'
        ),
        'Chování v salonu': 'Conduct in the salon',
        'Respektujte masérky a ostatní klienty': 'Respect masseuses and other clients',
        'V masážní místnosti vypínejte mobilní telefon': 'Turn off your mobile phone in the massage room',
        'Salon je místem relaxace — prosíme o klidný a diskrétní chování': (
            'The salon is a place of relaxation — please behave calmly and discreetly'
        ),
        'Masáž je poskytována výhradně v rámci profesionálních služeb': (
            'Massage is provided exclusively as a professional service'
        ),
        'Platba': 'Payment',
        'Platbu uhradíte po skončení masáže hotově nebo kartou dle aktuálních možností salonu. Aktuální ceník najdete na stránce': (
            'Payment is made after the massage in cash or by card according to current salon options. '
            'See the current price list on the'
        ),
        'Máte dotaz k pravidlům? Kontaktujte nás na': 'Have a question about the rules? Contact us at',
        'nebo': 'or',
        'Rozvrh masáží': 'Massage schedule',
        'Vyberte masérku a prohlédněte si její týdenní směny. Volné termíny rezervujte jedním kliknutím.': (
            'Choose a masseuse and view her weekly shifts. Book available slots with one click.'
        ),
        'Týdenní rozvrh': 'Weekly schedule',
        'Volný termín': 'Available slot',
        'Obsazeno': 'Booked',
        'Profil masérky': 'Masseuse profile',
        'Dnes': 'Today',
        'Volno': 'Day off',
        'Rozvrh bude brzy k dispozici.': 'The schedule will be available soon.',
        'Klikněte na volný termín pro přechod k rezervaci.': 'Click an available slot to proceed to booking.',
        'Máte otázky? Máme odpovědi': 'Have questions? We have answers',
        'Masáž a relaxace': 'Massage & relaxation',
        'v srdci Prahy': 'in the heart of Prague',
        'Navigace': 'Navigation',
        'Hlavní strana': 'Homepage',
        'Informace': 'Information',
        'Všechna práva vyhrazena.': 'All rights reserved.',
        'Vybrat jiný termín': 'Choose another slot',
        'Pokračovat': 'Continue',
        'Vybraná masáž:': 'Selected massage:',
        'Zpět': 'Back',
        'Vyberte termín': 'Choose a time slot',
        'Masáž': 'Massage',
        'Libovolná': 'Any',
        'Kontaktní údaje': 'Contact details',
        'Potvrzení rezervace': 'Booking confirmation',
        'Jméno': 'Name',
        'Poznámka': 'Note',
        'Potvrdit rezervaci': 'Confirm booking',
        'Rezervace potvrzena': 'Booking confirmed',
        'Potvrzení bylo odesláno na': 'Confirmation was sent to',
        'Těšíme se na vás!': 'We look forward to seeing you!',
        'Mobilní navigace': 'Mobile navigation',
        'Zavřít': 'Close',
        'Hlavní navigace': 'Main navigation',
        'Jazyk': 'Language',
        'Menu': 'Menu',
        'Informace o salonu': 'Salon information',
        'Zjistit více': 'Learn more',
        'praxe': 'experience',
        'Rezervace nenalezena': 'Booking not found',
        'Rezervujte si masáž online': 'Book your massage online',
        'Načítání...': 'Loading...',
        'Další masáže': 'More massages',
        'Relaxační a terapeutické masáže Praha': 'Relaxation & therapeutic massages Prague',
        'Každá masáž je individuálně přizpůsobena vašim potřebám. Vyberte si tu pravou pro váš dokonalý zážitek.': (
            'Each massage is individually tailored to your needs. Choose the right one for your perfect experience.'
        ),
        'Žádné masáže k dispozici.': 'No massages available.',
        'Specializace': 'Specializations',
        'Rezervovat s touto masérkou': 'Book with this masseuse',
        'Certifikované masérky s letitou praxí. Každá specializuje na jiné techniky masáže pro maximální komfort.': (
            'Certified masseuses with years of experience. Each specializes in different massage techniques for maximum comfort.'
        ),
        'Žádné masérky k dispozici.': 'No masseuses available.',
        'Cena od': 'Price from',
        'Délka': 'Duration',
        'Masérky pro tuto masáž': 'Masseuses for this massage',
        '1 rok': '1 year',
        '%s roky': '%s years',
        '%s let': '%s years',
    },
    'ru': {
        'Blog o masáži a relaxaci Praha | Black Velvet': 'Блог о массаже и релаксации Прага | Black Velvet',
        'Tipy, rady a články o masáži, relaxaci a wellness v Praze. Praktické informace od odborníků Black Velvet Spa.': (
            'Советы, рекомендации и статьи о массаже, релаксации и wellness в Праге. '
            'Практическая информация от экспертов Black Velvet Spa.'
        ),
        'Blog': 'Блог',
        'Domů': 'Главная',
        'Masáž a relaxace Praha — Luxusní spa salon | Black Velvet': (
            'Массаж и релаксация Прага — Роскошный spa-салон | Black Velvet'
        ),
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy. Aromaterapeutické, relaxační a sportovní masáže. Rezervujte online.': (
            'Black Velvet Spa — роскошный массажный салон в сердце Праги. '
            'Ароматерапевтический, расслабляющий и спортивный массаж. Бронируйте онлайн.'
        ),
        'Vaše jméno': 'Ваше имя',
        'Email': 'Email',
        'Telefon': 'Телефон',
        'Vaše zpráva': 'Ваше сообщение',
        'Ceník masáží Praha — Ceny a délky | Black Velvet': 'Прайс-лист массажа Прага — Цены и длительность | Black Velvet',
        'Kompletní ceník masáží v Black Velvet Spa Praha. Transparentní ceny aromaterapeutické, sportovní a relaxační masáže.': (
            'Полный прайс-лист массажа в Black Velvet Spa Прага. '
            'Прозрачные цены на ароматерапевтический, спортивный и расслабляющий массаж.'
        ),
        'Ceník': 'Прайс-лист',
        'Kontakt — Black Velvet Spa Vinohrady, Praha 2': 'Контакты — Black Velvet Spa Винограды, Прага 2',
        'Kontaktujte Black Velvet Spa ve Vinohradech, Praha 2. Adresa Lužická 1416/29, telefon, email a kontaktní formulář. Rezervace masáže online nebo telefonicky.': (
            'Свяжитесь с Black Velvet Spa в Виноградах, Прага 2. Адрес Lužická 1416/29, телефон, email и контактная форма. '
            'Запись на массаж онлайн или по телефону.'
        ),
        'Kontakt': 'Контакты',
        'Zpráva byla odeslána. Brzy se vám ozveme.': 'Сообщение отправлено. Мы скоро свяжемся с вами.',
        'Rozvrh masérek Praha — Otevírací doba | Black Velvet': 'Расписание массажисток Прага — Часы работы | Black Velvet',
        'Rozvrh masérek a otevírací doba Black Velvet Spa ve Vinohradech, Praha 2. Aktuální směny a volné termíny pro rezervaci masáže.': (
            'Расписание массажисток и часы работы Black Velvet Spa в Виноградах, Прага 2. '
            'Актуальные смены и свободные слоты для записи на массаж.'
        ),
        'Rozvrh': 'Расписание',
        'O nás — Luxusní masážní salon Praha | Black Velvet': 'О нас — Роскошный массажный салон Прага | Black Velvet',
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy 1. Profesionální masérky, klidné prostředí a individuální péče.': (
            'Black Velvet Spa — роскошный массажный салон в сердце Праги 1. '
            'Профессиональные массажистки, спокойная атмосфера и индивидуальный подход.'
        ),
        'O nás': 'О нас',
        'Pravidla salonu | Black Velvet Spa Praha': 'Правила салона | Black Velvet Spa Прага',
        'Pravidla a zásady návštěvy Black Velvet Spa. Rezervace, zrušení termínu, hygiena a chování v salonu.': (
            'Правила и принципы посещения Black Velvet Spa. '
            'Бронирование, отмена, гигиена и поведение в салоне.'
        ),
        'Pravidla salonu': 'Правила салона',
        'Zásady ochrany osobních údajů | Black Velvet': 'Политика конфиденциальности | Black Velvet',
        'Zásady ochrany osobních údajů Black Velvet Spa. Informace o zpracování dat a vašich právech.': (
            'Политика конфиденциальности Black Velvet Spa. Информация об обработке данных и ваших правах.'
        ),
        'Zásady ochrany': 'Конфиденциальность',
        'Vyberte masáž': 'Выберите массаж',
        'Vyberte masérku': 'Выберите массажистку',
        'Libovolná masérka': 'Любая массажистка',
        'Datum': 'Дата',
        'Čas': 'Время',
        'Datum musí být v budoucnosti.': 'Дата должна быть в будущем.',
        'Jméno a příjmení': 'Имя и фамилия',
        'Poznámka (volitelné)': 'Примечание (необязательно)',
        'Rezervace masáže Praha — Online booking | Black Velvet': 'Запись на массаж Прага — Онлайн-бронирование | Black Velvet',
        'Rezervujte masáž online v Black Velvet Spa Praha. Vyberte službu, masérku, termín a potvrďte rezervaci.': (
            'Запишитесь на массаж онлайн в Black Velvet Spa Прага. '
            'Выберите услугу, массажистку, время и подтвердите бронирование.'
        ),
        'Rezervace': 'Бронирование',
        'Služba': 'Услуга',
        'Masérka': 'Массажистка',
        'Termín': 'Время записи',
        'Potvrzení': 'Подтверждение',
        'Tento termín je již obsazený. Vyberte prosím jiný.': 'Это время уже занято. Пожалуйста, выберите другое.',
        'Potvrzení rezervace — Black Velvet Spa': 'Подтверждение бронирования — Black Velvet Spa',
        'Dobrý den {name},\n\nVaše rezervace byla potvrzena.\nSlužba: {service}\nTermín: {date} {time}\n\nPotvrzení: {url}': (
            'Здравствуйте, {name},\n\nВаше бронирование подтверждено.\nУслуга: {service}\n'
            'Время: {date} {time}\n\nПодтверждение: {url}'
        ),
        'Relaxační a terapeutické masáže Praha | Black Velvet': 'Расслабляющий и терапевтический массаж Прага | Black Velvet',
        'Kompletní nabídka masáží v Praze — aromaterapeutická, klasická, sportovní, relaxační a lymfatická. Rezervujte termín online.': (
            'Полный ассортимент массажа в Праге — ароматерапевтический, классический, '
            'спортивный, расслабляющий и лимфодренажный. Запишитесь онлайн.'
        ),
        'Masáže': 'Массаж',
        'Naše masérky Praha — Odbornice Black Velvet Spa': 'Наши массажистки Прага — Эксперты Black Velvet Spa',
        'Seznamte se s našimi certifikovanými masérkami v Praze. Aromaterapie, sportovní a relaxační masáže od profesionálek.': (
            'Познакомьтесь с нашими сертифицированными массажистками в Праге. '
            'Ароматерапия, спортивный и расслабляющий массаж от профессионалов.'
        ),
        'Masérky': 'Массажистки',
        'Související články': 'Похожие статьи',
        'Tipy a rady o masáži a relaxaci': 'Советы и рекомендации о массаже и релаксации',
        'Zatím žádné články.': 'Пока нет статей.',
        'Stránkování': 'Пагинация',
        'Stránka nenalezena.': 'Страница не найдена.',
        'Zpět na hlavní stranu': 'Вернуться на главную',
        'Došlo k chybě serveru. Zkuste to prosím později.': 'Произошла ошибка сервера. Пожалуйста, попробуйте позже.',
        'Masáž a relaxace Praha': 'Массаж и релаксация Прага',
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy. Odhalte svůj vlastní ráj.': (
            'Black Velvet Spa — роскошный массажный салон в сердце Праги. Откройте свой собственный рай.'
        ),
        'Rezervovat': 'Записаться',
        'Naše masáže': 'Наши массажи',
        'Masáže pro tělo i duši': 'Массаж для тела и души',
        'Všechny masáže': 'Все массажи',
        'Odbornice pro váš komfort a relaxaci': 'Эксперты для вашего комфорта и релаксации',
        'Všechny masérky': 'Все массажистки',
        'Čtyři kroky k dokonalé relaxaci': 'Четыре шага к идеальной релаксации',
        'Prohlédněte si nabídku a vyberte masáž, která vám nejvíce vyhovuje.': (
            'Ознакомьтесь с предложением и выберите массаж, который вам больше всего подходит.'
        ),
        'Rezervujte termín': 'Запишитесь на приём',
        'Online přes náš systém nebo telefonicky — rychle a jednoduše.': (
            'Онлайн через нашу систему или по телефону — быстро и просто.'
        ),
        'Přijďte a relaxujte': 'Приходите и расслабляйтесь',
        'Uvítáme vás v salonu a připravíme vše pro dokonalý zážitek.': (
            'Мы встретим вас в салоне и подготовим всё для идеального опыта.'
        ),
        'Odejděte odpočatí': 'Уходите отдохнувшими',
        'Odnesete si hluboký klid a regeneraci pro tělo i mysl.': (
            'Вы унесёте с собой глубокое спокойствие и восстановление для тела и разума.'
        ),
        'Co říkají naši klienti': 'Что говорят наши клиенты',
        'Zobrazit kontakt a mapu': 'Показать контакты и карту',
        'Kontakt a mapa': 'Контакты и карта',
        'Najdete nás v srdci Prahy': 'Мы находимся в сердце Праги',
        'Otevírací doba': 'Часы работы',
        'Denně od 9:00 do 5:00 ráno': 'Ежедневно с 9:00 до 5:00 утра',
        'Odhalte svůj vlastní ráj': 'Откройте свой собственный рай',
        'Rezervovat masáž': 'Записаться на массаж',
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy, kde se setkává profesionalita s klidem a diskrétní atmosférou.': (
            'Black Velvet Spa — роскошный массажный салон в сердце Праги, '
            'где профессионализм сочетается со спокойствием и дискретной атмосферой.'
        ),
        'Náš příběh': 'Наша история',
        'Vytvořili jsme prostor, kde se můžete plně uvolnit a na chvíli zapomenout na každodenní shon. Každá masáž je vedena zkušenými masérkami, které dbají na vaše individuální potřeby a komfort.': (
            'Мы создали пространство, где вы можете полностью расслабиться и на время забыть о повседневной суете. '
            'Каждый массаж проводят опытные массажистки, которые заботятся о ваших индивидуальных потребностях и комфорте.'
        ),
        'Co nás odlišuje': 'Чем мы отличаемся',
        'Profesionální tým certifikovaných masérek': 'Профессиональная команда сертифицированных массажисток',
        'Klidné a diskrétní prostředí v centru Prahy 1': 'Спокойная и дискретная обстановка в центре Праги 1',
        'Široká nabídka relaxačních a terapeutických masáží': 'Широкий выбор расслабляющего и терапевтического массажа',
        'Jednoduchá online rezervace termínů': 'Простое онлайн-бронирование',
        'Naše hodnoty': 'Наши ценности',
        'Respekt, diskrétnost a péče o detail jsou pro nás základem každé návštěvy. Věříme, že kvalitní masáž obnovuje tělo i mysl — a proto klademe důraz na osobní přístup ke každému klientovi.': (
            'Уважение, дискретность и внимание к деталям — основа каждого визита. '
            'Мы верим, что качественный массаж восстанавливает тело и разум — поэтому уделяем внимание индивидуальному подходу к каждому клиенту.'
        ),
        'Kontaktujte nás': 'Свяжитесь с нами',
        'Máte dotaz nebo chcete rezervovat termín? Jsme tu pro vás.': (
            'Есть вопрос или хотите записаться? Мы здесь для вас.'
        ),
        'Rychlý kontakt': 'Быстрый контакт',
        'Adresa': 'Адрес',
        'Kde nás najdete': 'Где нас найти',
        'Mapa — Black Velvet Spa Praha': 'Карта — Black Velvet Spa Прага',
        'Otevřít v Mapách': 'Открыть в Картах',
        'Zkontrolujte prosím vyplněná pole.': 'Пожалуйста, проверьте заполненные поля.',
        'Odeslat zprávu': 'Отправить сообщение',
        'Zpráva odeslána': 'Сообщение отправлено',
        'Děkujeme. Brzy se vám ozveme.': 'Спасибо. Мы скоро свяжемся с вами.',
        'Ceník masáží Praha': 'Прайс-лист массажа Прага',
        'Transparentní ceny všech masáží v Black Velvet Spa. Všechny ceny jsou uvedeny včetně DPH.': (
            'Прозрачные цены на все виды массажа в Black Velvet Spa. Все цены указаны с учётом НДС.'
        ),
        'Ceník podle délky masáže': 'Прайс-лист по длительности массажа',
        'Délka masáže': 'Длительность массажа',
        'min': 'мин',
        'Ceník bude brzy k dispozici.': 'Прайс-лист скоро будет доступен.',
        'Zásady ochrany osobních údajů': 'Политика конфиденциальности',
        'Black Velvet Spa zpracovává osobní údaje v souladu s nařízením GDPR a platnými právními předpisy České republiky.': (
            'Black Velvet Spa обрабатывает персональные данные в соответствии с GDPR '
            'и действующим законодательством Чешской Республики.'
        ),
        'Správce údajů': 'Контролёр данных',
        'Účel zpracování': 'Цель обработки',
        'Osobní údaje zpracováváme za účelem rezervace masáží, komunikace s klienty a plnění smluvních povinností.': (
            'Мы обрабатываем персональные данные для бронирования массажа, '
            'общения с клиентами и выполнения договорных обязательств.'
        ),
        'Vaše práva': 'Ваши права',
        'Máte právo na přístup, opravu, výmaz a přenositelnost údajů. Kontaktujte nás na': (
            'Вы имеете право на доступ, исправление, удаление и переносимость данных. Свяжитесь с нами по'
        ),
        'Aby byl váš zážitek co nejpříjemnější pro vás i ostatní klienty, prosíme o dodržování následujících zásad.': (
            'Чтобы ваш визит был максимально приятным для вас и других клиентов, '
            'просим соблюдать следующие правила.'
        ),
        'Rezervace a dochvilnost': 'Бронирование и пунктуальность',
        'Termín rezervujte předem online nebo telefonicky. Doporučujeme dorazit 5–10 minut před začátkem masáže. Při zpoždění může být délka masáže zkrácena bez snížení ceny.': (
            'Записывайтесь заранее онлайн или по телефону. Рекомендуем прибыть за 5–10 минут до начала массажа. '
            'При опоздании длительность массажа может быть сокращена без снижения цены.'
        ),
        'Zrušení termínu': 'Отмена записи',
        'Rezervaci zrušte nejpozději 24 hodin předem telefonicky nebo e-mailem. Při pozdním zrušení nebo nedostavení se si vyhrazujeme právo účtovat storno poplatek.': (
            'Отмените бронирование не позднее чем за 24 часа по телефону или email. '
            'При поздней отмене или неявке мы оставляем за собой право взимать штраф.'
        ),
        'Hygiena a zdraví': 'Гигиена и здоровье',
        'Před masáží se prosím osprchujte. Při akutních infekcích, horečce nebo kožních onemocněních masáž odložte. Informujte masérku o alergiích, zraněních nebo zdravotních omezeních.': (
            'Пожалуйста, примите душ перед массажем. При острых инфекциях, '
            'лихорадке или кожных заболеваниях отложите массаж. Сообщите массажистке об аллергиях, травмах или ограничениях по здоровью.'
        ),
        'Chování v salonu': 'Поведение в салоне',
        'Respektujte masérky a ostatní klienty': 'Уважайте массажисток и других клиентов',
        'V masážní místnosti vypínejte mobilní telefon': 'Выключайте мобильный телефон в массажном кабинете',
        'Salon je místem relaxace — prosíme o klidný a diskrétní chování': (
            'Салон — место для релаксации — просим вести себя спокойно и дискретно'
        ),
        'Masáž je poskytována výhradně v rámci profesionálních služeb': (
            'Массаж предоставляется исключительно в рамках профессиональных услуг'
        ),
        'Platba': 'Оплата',
        'Platbu uhradíte po skončení masáže hotově nebo kartou dle aktuálních možností salonu. Aktuální ceník najdete na stránce': (
            'Оплату производите после массажа наличными или картой в соответствии с возможностями салона. '
            'Актуальный прайс-лист на странице'
        ),
        'Máte dotaz k pravidlům? Kontaktujte nás na': 'Есть вопрос по правилам? Свяжитесь с нами по',
        'nebo': 'или',
        'Rozvrh masáží': 'Расписание массажа',
        'Vyberte masérku a prohlédněte si její týdenní směny. Volné termíny rezervujte jedním kliknutím.': (
            'Выберите массажистку и просмотрите её недельное расписание. Свободные слоты — в один клик.'
        ),
        'Týdenní rozvrh': 'Недельное расписание',
        'Volný termín': 'Свободный слот',
        'Obsazeno': 'Занято',
        'Profil masérky': 'Профиль массажистки',
        'Dnes': 'Сегодня',
        'Volno': 'Выходной',
        'Rozvrh bude brzy k dispozici.': 'Расписание скоро будет доступно.',
        'Klikněte na volný termín pro přechod k rezervaci.': 'Нажмите на свободный слот для перехода к бронированию.',
        'Máte otázky? Máme odpovědi': 'Есть вопросы? У нас есть ответы',
        'Masáž a relaxace': 'Массаж и релаксация',
        'v srdci Prahy': 'в сердце Праги',
        'Navigace': 'Навигация',
        'Hlavní strana': 'Главная',
        'Informace': 'Информация',
        'Všechna práva vyhrazena.': 'Все права защищены.',
        'Vybrat jiný termín': 'Выбрать другое время',
        'Pokračovat': 'Продолжить',
        'Vybraná masáž:': 'Выбранный массаж:',
        'Zpět': 'Назад',
        'Vyberte termín': 'Выберите время',
        'Masáž': 'Массаж',
        'Libovolná': 'Любая',
        'Kontaktní údaje': 'Контактные данные',
        'Potvrzení rezervace': 'Подтверждение бронирования',
        'Jméno': 'Имя',
        'Poznámka': 'Примечание',
        'Potvrdit rezervaci': 'Подтвердить бронирование',
        'Rezervace potvrzena': 'Бронирование подтверждено',
        'Potvrzení bylo odesláno na': 'Подтверждение отправлено на',
        'Těšíme se na vás!': 'Ждём вас!',
        'Mobilní navigace': 'Мобильная навигация',
        'Zavřít': 'Закрыть',
        'Hlavní navigace': 'Главная навигация',
        'Jazyk': 'Язык',
        'Menu': 'Меню',
        'Informace o salonu': 'Информация о салоне',
        'Zjistit více': 'Узнать больше',
        'praxe': 'опыт',
        'Rezervace nenalezena': 'Бронирование не найдено',
        'Rezervujte si masáž online': 'Запишитесь на массаж онлайн',
        'Načítání...': 'Загрузка...',
        'Další masáže': 'Другие массажи',
        'Relaxační a terapeutické masáže Praha': 'Расслабляющий и терапевтический массаж Прага',
        'Každá masáž je individuálně přizpůsobena vašim potřebám. Vyberte si tu pravou pro váš dokonalý zážitek.': (
            'Каждый массаж индивидуально адаптирован под ваши потребности. Выберите подходящий для идеального опыта.'
        ),
        'Žádné masáže k dispozici.': 'Нет доступных массажей.',
        'Specializace': 'Специализация',
        'Rezervovat s touto masérkou': 'Записаться к этой массажистке',
        'Certifikované masérky s letitou praxí. Každá specializuje na jiné techniky masáže pro maximální komfort.': (
            'Сертифицированные массажистки с многолетним опытом. Каждая специализируется на разных техниках массажа для максимального комфорта.'
        ),
        'Žádné masérky k dispozici.': 'Нет доступных массажисток.',
        'Cena od': 'Цена от',
        'Délka': 'Длительность',
        'Masérky pro tuto masáž': 'Массажистки для этого массажа',
        '1 rok': '1 год',
        '%s roky': '%s года',
        '%s let': '%s лет',
    },
}


def fill_locale(lang: str) -> list[str]:
    po_path = BASE / lang / 'LC_MESSAGES' / 'django.po'
    po = polib.pofile(str(po_path))
    missing = []
    for entry in po:
        if not entry.msgid:
            continue
        translation = TRANSLATIONS[lang].get(entry.msgid)
        if translation is None:
            missing.append(entry.msgid)
            continue
        entry.msgstr = translation
    po.metadata['Language'] = lang
    if 'fuzzy' in po.metadata:
        del po.metadata['fuzzy']
    po.save(str(po_path))
    return missing


def main():
    for lang in ('en', 'ru'):
        missing = fill_locale(lang)
        if missing:
            print(f'[{lang}] Missing translations ({len(missing)}):')
            for msgid in missing:
                print(f'  - {msgid[:80]}...' if len(msgid) > 80 else f'  - {msgid}')
        else:
            print(f'[{lang}] All translations filled.')


if __name__ == '__main__':
    main()
