/**
 * Heat-Air Stress Advisor - survey forms (2026CSAE102 Milestone 1)
 *
 * HOW TO USE (2 minutes):
 * 1. Go to https://script.google.com and click New project.
 * 2. Delete the default code, paste this whole file, and click Save.
 * 3. Choose the function createAllForms in the toolbar and click Run.
 * 4. Allow the permissions when asked (it only creates Google Forms in your Drive).
 * 5. Open View > Logs (or Execution log) to see the links for both forms.
 *    - "Share link" is what you send to respondents.
 *    - "Edit link" is for your team.
 * 6. In each form, open the Responses tab and click "Link to Sheets" to collect answers.
 *
 * Form A: outdoor workers (Hindi + English). Form B: supervisors, employers, RWAs, NGOs, health professionals.
 * Both are anonymous. Do not add questions asking for names or phone numbers.
 */

function createAllForms() {
  var a = createWorkerForm();
  var b = createStakeholderForm();
  Logger.log('FORM A (workers) share link: ' + a.getPublishedUrl());
  Logger.log('FORM A (workers) edit link: ' + a.getEditUrl());
  Logger.log('FORM B (stakeholders) share link: ' + b.getPublishedUrl());
  Logger.log('FORM B (stakeholders) edit link: ' + b.getEditUrl());
}

// ---------- helpers ----------
function single(form, title, choices, required, other, help) {
  var it = form.addMultipleChoiceItem().setTitle(title).setChoiceValues(choices).setRequired(required);
  if (other) it.showOtherOption(true);
  if (help) it.setHelpText(help);
  return it;
}
function multi(form, title, choices, required, other, help) {
  var it = form.addCheckboxItem().setTitle(title).setChoiceValues(choices).setRequired(required);
  if (other) it.showOtherOption(true);
  if (help) it.setHelpText(help);
  return it;
}
function dropdown(form, title, choices, required) {
  return form.addListItem().setTitle(title).setChoiceValues(choices).setRequired(required);
}
function scale(form, title, low, high, required) {
  return form.addScaleItem().setTitle(title).setBounds(1, 5).setLabels(low, high).setRequired(required);
}
function paragraph(form, title, required, help) {
  var it = form.addParagraphTextItem().setTitle(title).setRequired(required);
  if (help) it.setHelpText(help);
  return it;
}

// ---------- FORM A: outdoor workers ----------
function createWorkerForm() {
  var f = FormApp.create('Heat and Air Pollution at Work - Worker Survey / गर्मी और प्रदूषण: कामगार सर्वे');
  f.setCollectEmail(false);
  f.setLimitOneResponsePerUser(false);
  f.setAllowResponseEdits(false);
  f.setProgressBar(true);
  f.setConfirmationMessage('Thank you! / धन्यवाद! आपके जवाब हमारे कॉलेज प्रोजेक्ट में मदद करेंगे।');
  f.setDescription(
    'We are B.Tech students at Bennett University working on a college project about heat and air pollution for outdoor workers in Delhi-NCR. ' +
    'This survey takes about 5 minutes. It is anonymous: please do NOT write your name or phone number. ' +
    'You can stop at any time. We will use answers only for the project. This is not medical advice.\n\n' +
    'हम बेनेट यूनिवर्सिटी के बी.टेक छात्र हैं और दिल्ली-एनसीआर के बाहर काम करने वाले लोगों के लिए गर्मी और प्रदूषण पर एक कॉलेज प्रोजेक्ट कर रहे हैं। ' +
    'इसमें लगभग 5 मिनट लगेंगे। यह गुमनाम है - कृपया अपना नाम या फ़ोन नंबर न लिखें। आप कभी भी रुक सकते हैं। ' +
    'जवाब सिर्फ़ प्रोजेक्ट के लिए इस्तेमाल होंगे। यह चिकित्सा सलाह नहीं है।'
  );

  multi(f, 'Consent / सहमति',
    ['I am 18 years or older and I agree to answer voluntarily. / मेरी उम्र 18 साल या उससे अधिक है और मैं अपनी मर्ज़ी से जवाब दे रहा/रही हूँ।'],
    true, false);

  single(f, '1. What is your main outdoor work? / आपका मुख्य बाहर का काम क्या है?',
    ['Delivery rider (food / grocery / parcel) / डिलीवरी राइडर',
     'Construction worker / निर्माण मज़दूर',
     'Street vendor / रेहड़ी-पटरी वाला',
     'Auto / e-rickshaw / cab driver / ऑटो, ई-रिक्शा या कैब चालक',
     'Security guard / सुरक्षा गार्ड',
     'Sanitation or waste worker / सफ़ाई कर्मचारी'],
    true, true);

  dropdown(f, '2. Which area do you mostly work in? / आप ज़्यादातर किस इलाके में काम करते हैं?',
    ['Delhi / दिल्ली', 'Noida / नोएडा', 'Greater Noida / ग्रेटर नोएडा', 'Gurugram / गुरुग्राम',
     'Faridabad / फ़रीदाबाद', 'Ghaziabad / गाज़ियाबाद', 'Other NCR area / अन्य'], true);

  single(f, '3. How many hours a day do you work outdoors? / आप दिन में कितने घंटे बाहर काम करते हैं?',
    ['Less than 4 hours / 4 घंटे से कम', '4 to 6 hours / 4 से 6 घंटे', '6 to 8 hours / 6 से 8 घंटे',
     '8 to 10 hours / 8 से 10 घंटे', 'More than 10 hours / 10 घंटे से ज़्यादा'], true, false);

  multi(f, '4. Which hours are hardest for you? (choose all that apply) / कौन से घंटे सबसे मुश्किल होते हैं?',
    ['6 am to 10 am / सुबह 6 से 10', '10 am to 12 noon / सुबह 10 से दोपहर 12', '12 noon to 4 pm / दोपहर 12 से 4',
     '4 pm to 7 pm / शाम 4 से 7', '7 pm to 11 pm / रात 7 से 11', 'Late night / देर रात'], true, false);

  multi(f, '5. In the hot months, which of these have you had while working? / गर्मी में काम करते समय आपको इनमें से क्या हुआ है?',
    ['Headache / सिरदर्द', 'Dizziness / चक्कर आना', 'Heavy sweating or weakness / बहुत पसीना या कमज़ोरी',
     'Nausea or vomiting / जी मिचलाना या उल्टी', 'Muscle cramps / मांसपेशियों में ऐंठन', 'Fainting / बेहोशी',
     'None of these / इनमें से कुछ नहीं'], true, true);

  multi(f, '6. In the smog months (Oct to Jan), which of these have you had? / धुंध (अक्टूबर से जनवरी) में आपको इनमें से क्या हुआ है?',
    ['Cough / खाँसी', 'Eye irritation / आँखों में जलन', 'Breathlessness / साँस फूलना',
     'Sore throat / गले में खराश', 'Headache / सिरदर्द', 'None of these / इनमें से कुछ नहीं'], true, true);

  multi(f, '7. How do you learn about weather or air quality? / मौसम या हवा की गुणवत्ता की जानकारी कैसे मिलती है?',
    ['TV or news / टीवी या समाचार', 'Phone weather app / मोबाइल मौसम ऐप', 'Air-quality (AQI) app / AQI ऐप',
     'WhatsApp or social media / व्हाट्सऐप या सोशल मीडिया',
     'Employer, platform or supervisor / मालिक, कंपनी या सुपरवाइज़र',
     'Other workers or family / साथी कामगार या परिवार', 'I do not check / मैं नहीं देखता/देखती'], true, true);

  single(f, '8. Do you change your work or rest because of heat or pollution? / क्या आप गर्मी या प्रदूषण की वजह से काम या आराम बदलते हैं?',
    ['Never / कभी नहीं', 'Rarely / कभी-कभार', 'Sometimes / कभी-कभी', 'Often / अक्सर', 'Always / हमेशा'], true, false);

  multi(f, '9. What stops you from resting or reducing work in bad conditions? / खराब मौसम में आराम करने या काम कम करने से आपको क्या रोकता है?',
    ['Loss of income or incentives / कमाई या इंसेंटिव का नुकसान',
     'Pressure from employer or platform / मालिक या कंपनी का दबाव',
     'No shade or place to rest / छाया या आराम की जगह नहीं',
     'No clear warning or advice / कोई साफ़ चेतावनी या सलाह नहीं'], true, true);

  single(f, '10. Do you use a smartphone with internet? / क्या आप इंटरनेट वाला स्मार्टफ़ोन इस्तेमाल करते हैं?',
    ['Yes, my own phone / हाँ, अपना फ़ोन', 'Yes, a shared phone / हाँ, साझा फ़ोन',
     'Basic phone, no internet / साधारण फ़ोन, इंटरनेट नहीं', 'No phone / फ़ोन नहीं'], true, false);

  single(f, '11. Preferred language for advice? / सलाह के लिए पसंदीदा भाषा?',
    ['Hindi / हिंदी', 'English / अंग्रेज़ी', 'Hinglish / हिंग्लिश'], true, true);

  multi(f, '12. How would you like to receive advice? / आप सलाह कैसे पाना चाहेंगे?',
    ['App or web link / ऐप या वेब लिंक', 'WhatsApp message / व्हाट्सऐप संदेश', 'SMS / एसएमएस',
     'Voice message or call / वॉइस संदेश या कॉल', 'Colour and picture chart / रंग और तस्वीर वाला चार्ट'], true, false);

  scale(f, '13. How useful would a simple colour-coded daily advice for your area be? / अपने इलाके के लिए रंग वाली सरल रोज़ की सलाह कितनी उपयोगी होगी?',
    'Not useful / उपयोगी नहीं', 'Very useful / बहुत उपयोगी', true);

  single(f, '14. When would you check it? / आप इसे कब देखेंगे?',
    ['Every morning / हर सुबह', 'Several times a day / दिन में कई बार',
     'Only when it feels very hot or smoky / जब बहुत गर्मी या धुआँ लगे', 'I would not check / मैं नहीं देखूँगा/देखूँगी'], true, false);

  single(f, '15. (Optional) Extra money you spend on water or cooling on a hot day? / (वैकल्पिक) गर्म दिन में पानी या ठंडक पर अतिरिक्त खर्च?',
    ['Nothing / कुछ नहीं', 'Up to Rs 30 / 30 रुपये तक', 'Rs 30 to 60 / 30 से 60 रुपये', 'More than Rs 60 / 60 रुपये से ज़्यादा'], false, false);

  paragraph(f, '16. (Optional) What advice would help you most? / (वैकल्पिक) कौन सी सलाह आपके सबसे ज़्यादा काम आएगी?', false,
    'Do not write your name or phone number. / अपना नाम या फ़ोन नंबर न लिखें।');

  return f;
}

// ---------- FORM B: stakeholders ----------
function createStakeholderForm() {
  var f = FormApp.create('Heat and Air Pollution for Outdoor Workers - Stakeholder Survey');
  f.setCollectEmail(false);
  f.setProgressBar(true);
  f.setConfirmationMessage('Thank you for your time. Your answers will help our college project.');
  f.setDescription(
    'We are B.Tech students at Bennett University working on a project about heat and air pollution advice for outdoor workers in Delhi-NCR. ' +
    'This survey is for supervisors, contractors, fleet managers, RWAs, NGOs and health professionals. It takes about 4 minutes and is anonymous: ' +
    'please do not enter names, phone numbers or company-confidential details. You can stop at any time.'
  );

  multi(f, 'Consent',
    ['I am 18 years or older and I agree to answer voluntarily.'], true, false);

  single(f, '1. Your role',
    ['Supervisor or contractor', 'Delivery fleet or platform operations', 'RWA, market or traders association',
     'NGO or worker union', 'Health professional', 'Government or municipal staff'], true, true);

  single(f, '2. Approximate number of outdoor workers you supervise or serve',
    ['Fewer than 10', '10 to 50', '51 to 200', 'More than 200'], true, false);

  multi(f, '3. What is done during extreme heat today?',
    ['Change working hours', 'Extra rest breaks', 'Drinking water or ORS provided', 'Shaded rest area',
     'Work stopped at peak hours', 'Nothing specific'], true, true);

  multi(f, '4. What is done during severe air pollution today?',
    ['Masks provided', 'Reduced outdoor work', 'Change working hours', 'Health check or advisory',
     'Nothing specific'], true, true);

  multi(f, '5. How do you get heat or air-quality alerts today?',
    ['IMD or weather app', 'AQI app (for example SAMEER)', 'TV or news', 'WhatsApp group',
     'Government or municipal message', 'I do not receive alerts'], true, true);

  scale(f, '6. Would a combined heat-air score for your area help you plan shifts or rest?',
    'Not helpful', 'Very helpful', true);

  multi(f, '7. Which features would matter most?',
    ['One simple colour score', 'Safer-hours timeline', 'Hindi and English advice', 'Job-specific advice',
     'WhatsApp delivery', 'Weekly area summary'], true, true);

  multi(f, '8. Main barriers to using such a tool',
    ['Workers do not have smartphones', 'Language or literacy', 'Trust in the information',
     'Income pressure on workers', 'Platform or employer policy', 'Privacy concerns'], true, true);

  paragraph(f, '9. (Optional) Any suggestion for us?', false, 'Please do not include names or phone numbers.');

  return f;
}
