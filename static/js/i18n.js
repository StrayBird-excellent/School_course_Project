// 多语言数据
const translations = {
  en: {
    // Header (通用)
    logo_text: "Breast Cancer AI Prediction Platform",
    page_title: "Breast Cancer Prediction",
    page_subtitle: "Predicts whether the tumor is benign or malignant with model accuracy above 95%",
    page_description: "Enter the 30 numeric features (mean, standard error, and \"worst\" values) from the Wisconsin diagnostic dataset.",
    
    // Tumor Cards
    benign_title: "Benign tumors",
    benign_desc: "Benign tumors are usually harmless; clinicians may monitor them instead of removing them. If you notice discomfort, pressure, or irritation, discuss options with your doctor so comfort can be improved.",
    malignant_title: "Malignant tumors",
    malignant_desc: "Malignant tumors are cancerous and can invade nearby tissue. When malignancy is suspected, a biopsy helps determine severity and guide treatment planning.",
    
    // Feature Input Section
    feature_input_title: "Feature Input",
    feature_input_mean: "Mean",
    feature_input_se: "Standard Error",
    feature_input_worst: "Worst",
    
    // Feature Labels (30 features)
    radius_mean: "Radius mean",
    texture_mean: "Texture mean",
    perimeter_mean: "Perimeter mean",
    area_mean: "Area mean",
    smoothness_mean: "Smoothness mean",
    compactness_mean: "Compactness mean",
    concavity_mean: "Concavity mean",
    concave_points_mean: "Concave points mean",
    symmetry_mean: "Symmetry mean",
    fractal_dimension_mean: "Fractal dimension mean",
    
    radius_se: "Radius se",
    texture_se: "Texture se",
    perimeter_se: "Perimeter se",
    area_se: "Area se",
    smoothness_se: "Smoothness se",
    compactness_se: "Compactness se",
    concavity_se: "Concavity se",
    concave_points_se: "Concave points se",
    symmetry_se: "Symmetry se",
    fractal_dimension_se: "Fractal dimension se",
    
    radius_worst: "Radius worst",
    texture_worst: "Texture worst",
    perimeter_worst: "Perimeter worst",
    area_worst: "Area worst",
    smoothness_worst: "Smoothness worst",
    compactness_worst: "Compactness worst",
    concavity_worst: "Concavity worst",
    concave_points_worst: "Concave points worst",
    symmetry_worst: "Symmetry worst",
    fractal_dimension_worst: "Fractal dimension worst",
    
    // Login Page
    hero_title: "AI-Driven Insights<br>For Better Outcomes",
    hero_subtitle: "Advanced AI models for early prediction, risk assessment, and personalized treatment guidance.",
    feature_1_title: "AI-Powered Prediction",
    feature_1_desc: "High-accuracy risk assessment using advanced machine learning algorithms.",
    feature_2_title: "Evidence-Based Insights",
    feature_2_desc: "Data-driven clinical decision support for healthcare professionals.",
    feature_3_title: "Secure & Private",
    feature_3_desc: "Enterprise-grade data protection and privacy compliance.",
    stat_1_label: "Model Accuracy",
    stat_2_label: "Cases Analyzed",
    stat_3_label: "Partner Hospitals",
    scroll_indicator: "Scroll to explore",
    login_title: "Welcome Back",
    login_subtitle: "Sign in to your account",
    placeholder_phone: "Phone number",
    placeholder_password: "Password",
    remember_me: "Remember me",
    forgot_password: "Forgot password?",
    btn_login: "Sign In",
    divider_text: "or continue with",
    social_google: "Google",
    social_microsoft: "Microsoft",
    footer_text: "Don't have an account?",
    footer_link: "Contact Admin",
    copyright: "© 2024 Breast Cancer AI Prediction Platform. All rights reserved.",
    footer_tagline: "Secure. Reliable. Intelligent.",
    
    // Home Page
    nav_home: "Home",
    nav_predict: "Prediction",
    nav_about: "About",
    nav_contact: "Contact",
    what_is_breast_cancer: "What is breast cancer",
    who_is_affected: "Who is affected",
    common_symptoms: "Common symptoms",
    breast_cancer_desc: "Cancers are usually named for the tissue where they start. Breast cancer begins in breast tissue. Like other cancers, it can grow into nearby tissue and spread to other parts of the body (metastasis).",
    who_affected_desc: "Breast cancer is a leading cause of cancer death in women (after lung cancer). About 1 in 8 women may develop invasive breast cancer in her lifetime. Screening and early detection remain important public health tools.",
    risk_factors: "Risk Factors",
    prevention_tips: "Prevention Tips",
    gender: "Gender",
    gender_desc: "Women are much more likely to develop breast cancer than men.",
    age: "Age",
    age_desc: "Risk increases with age, especially after 50.",
    family_history: "Family history",
    family_history_desc: "Having a close relative with breast cancer increases risk.",
    genetic_mutations: "Genetic mutations",
    genetic_mutations_desc: "BRCA1 and BRCA2 gene mutations increase risk.",
    hormone_therapy: "Hormone replacement therapy",
    hormone_therapy_desc: "Long-term use may increase risk.",
    obesity: "Obesity",
    obesity_desc: "Being overweight or obese increases risk, especially after menopause.",
    alcohol: "Alcohol consumption",
    alcohol_desc: "Drinking alcohol increases risk.",
    maintain_weight: "Maintain a healthy weight",
    exercise: "Exercise regularly (at least 150 minutes per week)",
    limit_alcohol: "Limit alcohol consumption",
    breastfeed: "Breastfeed if possible",
    screening: "Get regular screening mammograms",
    know_history: "Know your family history",
    symptoms_title: "Common Symptoms of Breast Cancer",
    symptom_intro: "Breast cancer can present with various symptoms. It's important to be aware of any changes in your breasts and consult a healthcare provider if you notice anything unusual.",
    common_symptoms_subtitle: "Common Symptoms",
    symptom_lump_detail: "A new lump or mass: Often painless, hard, and has irregular edges, but can also be soft, round, tender, or even painful.",
    symptom_size_change: "Change in breast size or shape: One breast may become larger or lower than the other.",
    symptom_nipple_detail: "Nipple changes: Nipple discharge (other than breast milk), nipple retraction (turning inward), or nipple skin that is scaly, crusty, or flaking.",
    symptom_skin_detail: "Skin changes: Dimpling, puckering, or redness of the breast skin, similar to the skin of an orange (peau d'orange).",
    symptom_pain_detail: "Breast or nipple pain: While most breast cancers are painless, some can cause pain.",
    symptom_swelling: "Swelling: Swelling of all or part of a breast (even if no lump is felt).",
    symptom_lymph_nodes: "Lymph node changes: Swelling of lymph nodes under the arm or around the collarbone.",
    when_to_see_doctor: "When to See a Doctor",
    see_doctor_intro: "You should consult a healthcare provider if you notice any of the following:",
    see_doctor_lump: "A new lump or mass in your breast or underarm",
    see_doctor_change: "Any change in the size, shape, or appearance of your breast",
    see_doctor_discharge: "Any discharge from your nipple",
    see_doctor_pain: "Persistent breast pain",
    see_doctor_skin: "Redness, scaliness, or thickening of the breast skin or nipple",
    see_doctor_inversion: "Nipple retraction or inversion",
    early_detection: "Importance of Early Detection",
    early_detection_desc: "Early detection of breast cancer greatly improves treatment outcomes. Regular self-exams, clinical breast exams, and mammograms are important screening tools. The American Cancer Society recommends:",
    early_detection_40_44: "Women aged 40-44 should have the choice to start annual mammograms",
    early_detection_45_54: "Women aged 45-54 should get annual mammograms",
    early_detection_55_plus: "Women aged 55+ should switch to mammograms every 2 years or continue annual screening",
    statistics_title: "Statistics",
    statistics_intro: "According to the American Cancer Society:",
    statistics_1_in_8_women: "About 1 in 8 women will develop invasive breast cancer during their lifetime",
    statistics_1_in_833_men: "About 1 in 833 men will develop breast cancer during their lifetime",
    statistics_early_detection_benefit: "Early detection through screening can significantly improve survival rates",
    feature_input: "Feature input",
    feature_input_desc: "Enter the 30 numeric features (mean, standard error, and \"worst\" values) from the Wisconsin diagnostic dataset.",
    generate_benign: "Generate Benign Data",
    generate_malignant: "Generate Malignant Data",
    generate_random: "Random Generation",
    run_prediction: "Run prediction",
    logout: "Logout",
    
    // Result Page
    prediction: "Prediction",
    probability_benign: "Benign",
    probability_malignant: "Malignant",
    model_accuracy: "Reported model accuracy (hold-out)",
    inference_time: "Inference time",
    back_to_form: "← Back to input form",
    prediction_details: "Prediction Details",
    probability_distribution: "Probability Distribution",
    medical_interpretation: "Medical Interpretation",
    benign_interpretation: "The model predicts that the tumor is benign (non-cancerous). This means the cells are not growing in an uncontrolled way and are unlikely to spread to other parts of the body. However, it's important to follow up with your healthcare provider for regular monitoring.",
    malignant_interpretation: "The model predicts that the tumor is malignant (cancerous). This means the cells are growing in an uncontrolled way and may have the potential to spread to other parts of the body. It's crucial to consult with a healthcare provider immediately for further evaluation and treatment options.",
    important_note: "Important Note",
    medical_disclaimer: "This prediction is based on a machine learning model and should not be considered a definitive medical diagnosis. Always consult with a qualified healthcare professional for proper medical advice.",
    generate_report: "Generate Report",
    report_description: "Create a detailed report of your prediction results for reference or to share with your healthcare provider.",
    download_report: "Download Report (HTML)",
    print_report: "Print Report",
    email_report: "Email Report",
    care_inspiration: "Care & Inspiration",
    care_subtitle: "Words of hope and encouragement for your journey",
    
    // Error Messages
    error_invalid_credentials: "Invalid email or password",
    error_empty_fields: "Please fill in all fields",
    error_server: "Server error, please try again later",
    
    // Language Options
    lang_english: "English",
    lang_chinese: "中文"
  },
  zh: {
    // Header (通用)
    logo_text: "乳腺癌AI预测平台",
    page_title: "乳腺癌预测",
    page_subtitle: "预测肿瘤是良性还是恶性，模型准确率超过95%",
    page_description: "输入威斯康星诊断数据集中的30个数值特征（平均值、标准误差和\"最差\"值）。",
    
    // Tumor Cards
    benign_title: "良性肿瘤",
    benign_desc: "良性肿瘤通常是无害的；临床医生可能会监测它们而不是切除。如果您感到不适、压迫或刺激，请与医生讨论选择，以便改善舒适度。",
    malignant_title: "恶性肿瘤",
    malignant_desc: "恶性肿瘤是癌性的，可以侵入邻近组织。当怀疑恶性时，活检有助于确定严重程度并指导治疗计划。",
    
    // Feature Input Section
    feature_input_title: "特征输入",
    feature_input_mean: "平均值",
    feature_input_se: "标准误差",
    feature_input_worst: "最差值",
    
    // Feature Labels (30 features)
    radius_mean: "半径平均值",
    texture_mean: "纹理平均值",
    perimeter_mean: "周长平均值",
    area_mean: "面积平均值",
    smoothness_mean: "平滑度平均值",
    compactness_mean: "致密性平均值",
    concavity_mean: "凹陷度平均值",
    concave_points_mean: "凹点平均值",
    symmetry_mean: "对称性平均值",
    fractal_dimension_mean: "分形维度平均值",
    
    radius_se: "半径标准误差",
    texture_se: "纹理标准误差",
    perimeter_se: "周长标准误差",
    area_se: "面积标准误差",
    smoothness_se: "平滑度标准误差",
    compactness_se: "致密性标准误差",
    concavity_se: "凹陷度标准误差",
    concave_points_se: "凹点标准误差",
    symmetry_se: "对称性标准误差",
    fractal_dimension_se: "分形维度标准误差",
    
    radius_worst: "半径最差值",
    texture_worst: "纹理最差值",
    perimeter_worst: "周长最差值",
    area_worst: "面积最差值",
    smoothness_worst: "平滑度最差值",
    compactness_worst: "致密性最差值",
    concavity_worst: "凹陷度最差值",
    concave_points_worst: "凹点最差值",
    symmetry_worst: "对称性最差值",
    fractal_dimension_worst: "分形维度最差值",
    
    // Login Page
    hero_title: "AI驱动的洞察<br>助力更好的治疗效果",
    hero_subtitle: "先进的AI模型用于早期预测、风险评估和个性化治疗指导。",
    feature_1_title: "AI驱动预测",
    feature_1_desc: "使用先进机器学习算法进行高精度风险评估。",
    feature_2_title: "循证医学洞察",
    feature_2_desc: "为医疗专业人员提供数据驱动的临床决策支持。",
    feature_3_title: "安全保密",
    feature_3_desc: "企业级数据保护和隐私合规。",
    stat_1_label: "模型准确率",
    stat_2_label: "分析案例数",
    stat_3_label: "合作医院",
    scroll_indicator: "向下滚动探索",
    login_title: "欢迎回来",
    login_subtitle: "登录您的账户",
    placeholder_phone: "手机号",
    placeholder_password: "密码",
    remember_me: "记住我",
    forgot_password: "忘记密码？",
    btn_login: "登录",
    divider_text: "或使用以下方式登录",
    social_google: "谷歌",
    social_microsoft: "微软",
    footer_text: "还没有账户？",
    footer_link: "联系管理员",
    copyright: "© 2024 乳腺癌AI预测平台. 保留所有权利.",
    footer_tagline: "安全. 可靠. 智能.",
    
    // Home Page
    nav_home: "首页",
    nav_predict: "预测",
    nav_about: "关于",
    nav_contact: "联系我们",
    what_is_breast_cancer: "什么是乳腺癌",
    who_is_affected: "谁会受影响",
    common_symptoms: "常见症状",
    breast_cancer_desc: "癌症通常以其起源组织命名。乳腺癌起源于乳腺组织。与其他癌症一样，它可以生长到邻近组织并扩散到身体其他部位（转移）。",
    who_affected_desc: "乳腺癌是女性癌症死亡的主要原因（仅次于肺癌）。大约每8名女性中就有1名可能在其一生中患上浸润性乳腺癌。筛查和早期发现仍然是重要的公共卫生工具。",
    risk_factors: "风险因素",
    prevention_tips: "预防建议",
    gender: "性别",
    gender_desc: "女性患乳腺癌的可能性远高于男性。",
    age: "年龄",
    age_desc: "风险随年龄增长而增加，尤其是50岁以后。",
    family_history: "家族史",
    family_history_desc: "有近亲患有乳腺癌会增加风险。",
    genetic_mutations: "基因突变",
    genetic_mutations_desc: "BRCA1和BRCA2基因突变会增加风险。",
    hormone_therapy: "激素替代疗法",
    hormone_therapy_desc: "长期使用可能会增加风险。",
    obesity: "肥胖",
    obesity_desc: "超重或肥胖会增加风险，尤其是绝经后。",
    alcohol: "饮酒",
    alcohol_desc: "饮酒会增加风险。",
    maintain_weight: "保持健康体重",
    exercise: "定期锻炼（每周至少150分钟）",
    limit_alcohol: "限制饮酒",
    breastfeed: "尽可能母乳喂养",
    screening: "定期进行乳腺筛查",
    know_history: "了解家族病史",
    symptoms_title: "乳腺癌的常见症状",
    symptom_intro: "乳腺癌可能表现出各种症状。注意乳房的任何变化很重要，如果发现任何异常，请咨询医疗保健提供者。",
    common_symptoms_subtitle: "常见症状",
    symptom_lump_detail: "新的肿块或肿物：通常无痛、坚硬且边缘不规则，但也可能柔软、圆形、有触痛，甚至疼痛。",
    symptom_size_change: "乳房大小或形状变化：一侧乳房可能变得比另一侧更大或下垂。",
    symptom_nipple_detail: "乳头变化：乳头溢液（非乳汁）、乳头内陷（向内凹陷）或乳头皮肤鳞屑、结痂或脱落。",
    symptom_skin_detail: "皮肤变化：乳房皮肤凹陷、褶皱或发红，类似橘皮（橘皮样变）。",
    symptom_pain_detail: "乳房或乳头疼痛：虽然大多数乳腺癌是无痛的，但有些会引起疼痛。",
    symptom_swelling: "肿胀：整个乳房或部分乳房肿胀（即使没有感觉到肿块）。",
    symptom_lymph_nodes: "淋巴结变化：腋下或锁骨周围淋巴结肿胀。",
    when_to_see_doctor: "何时就医",
    see_doctor_intro: "如果您发现以下任何情况，应咨询医疗保健提供者：",
    see_doctor_lump: "乳房或腋下出现新的肿块或肿物",
    see_doctor_change: "乳房大小、形状或外观的任何变化",
    see_doctor_discharge: "乳头有任何溢液",
    see_doctor_pain: "持续性乳房疼痛",
    see_doctor_skin: "乳房皮肤或乳头发红、鳞屑或增厚",
    see_doctor_inversion: "乳头回缩或内陷",
    early_detection: "早期检测的重要性",
    early_detection_desc: "早期检测乳腺癌可显著改善治疗效果。定期自我检查、临床乳房检查和乳房X光检查是重要的筛查工具。美国癌症协会建议：",
    early_detection_40_44: "40-44岁的女性应选择开始每年进行乳房X光检查",
    early_detection_45_54: "45-54岁的女性应每年进行乳房X光检查",
    early_detection_55_plus: "55岁以上的女性应每2年进行一次乳房X光检查，或继续每年筛查",
    statistics_title: "统计数据",
    statistics_intro: "根据美国癌症协会：",
    statistics_1_in_8_women: "大约每8名女性中就有1名可能在其一生中患上浸润性乳腺癌",
    statistics_1_in_833_men: "大约每833名男性中就有1名可能在其一生中患上乳腺癌",
    statistics_early_detection_benefit: "通过筛查进行早期检测可显著提高存活率",
    feature_input: "特征输入",
    feature_input_desc: "输入威斯康星诊断数据集中的30个数值特征（平均值、标准误差和\"最差\"值）。",
    generate_benign: "生成良性数据",
    generate_malignant: "生成恶性数据",
    generate_random: "随机生成",
    run_prediction: "运行预测",
    logout: "登出",
    
    // Result Page
    prediction: "预测结果",
    probability_benign: "良性",
    probability_malignant: "恶性",
    model_accuracy: "模型准确率（保留集）",
    inference_time: "推理时间",
    back_to_form: "← 返回输入表单",
    prediction_details: "预测详情",
    probability_distribution: "概率分布",
    medical_interpretation: "医学解释",
    benign_interpretation: "模型预测肿瘤为良性（非癌性）。这意味着细胞没有失控生长，不太可能扩散到身体其他部位。然而，重要的是要与您的医疗保健提供者跟进进行定期监测。",
    malignant_interpretation: "模型预测肿瘤为恶性（癌性）。这意味着细胞正在失控生长，并可能有潜力扩散到身体其他部位。立即咨询医疗保健提供者进行进一步评估和治疗选择至关重要。",
    important_note: "重要提示",
    medical_disclaimer: "此预测基于机器学习模型，不应被视为明确的医学诊断。请始终咨询合格的医疗专业人员以获得适当的医疗建议。",
    generate_report: "生成报告",
    report_description: "创建预测结果的详细报告，供参考或与您的医疗保健提供者分享。",
    download_report: "下载报告（HTML）",
    print_report: "打印报告",
    email_report: "邮件报告",
    care_inspiration: "关怀与鼓励",
    care_subtitle: "为您的旅程送上希望与鼓励的话语",
    
    // Error Messages
    error_invalid_credentials: "邮箱或密码无效",
    error_empty_fields: "请填写所有字段",
    error_server: "服务器错误，请稍后重试",
    
    // Language Options
    lang_english: "English",
    lang_chinese: "中文"
  }
};

// 获取当前语言
function getCurrentLanguage() {
  // 优先从localStorage获取
  const savedLang = localStorage.getItem('app_language');
  if (savedLang && translations[savedLang]) {
    return savedLang;
  }
  
  // 检测浏览器语言
  const browserLang = navigator.language || navigator.userLanguage;
  if (browserLang.startsWith('zh')) {
    return 'zh';
  }
  
  // 默认英语
  return 'en';
}

// 设置语言
function setLanguage(lang) {
  if (translations[lang]) {
    localStorage.setItem('app_language', lang);
    document.documentElement.lang = lang;
    updatePageContent(lang);
    updateLanguageSelector(lang);
  }
}

// 更新页面内容
function updatePageContent(lang) {
  const trans = translations[lang];
  
  if (!trans) {
    console.error('翻译数据不存在:', lang);
    return;
  }
  
  console.log('=== 正在更新页面内容, 语言:', lang);
  
  // 更新所有带有data-i18n属性的元素
  const i18nElements = document.querySelectorAll('[data-i18n]');
  console.log('找到', i18nElements.length, '个需要翻译的元素');
  
  i18nElements.forEach(element => {
    try {
      const key = element.getAttribute('data-i18n');
      if (trans[key]) {
        // 处理包含HTML的内容
        const tagName = element.tagName;
        if (tagName === 'H1' || tagName === 'H2' || tagName === 'H3' || tagName === 'H4' || tagName === 'P' || tagName === 'LI' || tagName === 'DIV' || tagName === 'SPAN' || tagName === 'A' || tagName === 'BUTTON') {
          element.innerHTML = trans[key];
        } else {
          element.textContent = trans[key];
        }
      } else {
        console.warn('未找到翻译:', key);
      }
    } catch (e) {
      console.error('更新元素失败:', element, e);
    }
  });
  
  // 更新placeholder
  const placeholderElements = document.querySelectorAll('[data-i18n-placeholder]');
  console.log('找到', placeholderElements.length, '个需要更新placeholder的元素');
  
  placeholderElements.forEach(element => {
    try {
      const key = element.getAttribute('data-i18n-placeholder');
      console.log('处理placeholder元素:', element.id, 'key:', key, 'trans[key]:', trans[key]);
      if (trans[key]) {
        element.placeholder = trans[key];
        console.log('已更新placeholder为:', trans[key]);
      } else {
        console.warn('未找到placeholder翻译:', key);
      }
    } catch (e) {
      console.error('更新placeholder失败:', element, e);
    }
  });
  
  // 更新alt属性
  document.querySelectorAll('[data-i18n-alt]').forEach(element => {
    try {
      const key = element.getAttribute('data-i18n-alt');
      if (trans[key]) {
        element.alt = trans[key];
      }
    } catch (e) {
      console.error('更新alt属性失败:', element, e);
    }
  });
  
  console.log('=== 页面内容更新完成 ===');
}

// 更新语言选择器显示
function updateLanguageSelector(lang) {
  const currentLang = document.getElementById('currentLanguage');
  if (currentLang) {
    currentLang.textContent = translations[lang][lang === 'zh' ? 'lang_chinese' : 'lang_english'];
  }
}

// 初始化语言设置
function initLanguage() {
  const lang = getCurrentLanguage();
  document.documentElement.lang = lang;
  updatePageContent(lang);
  updateLanguageSelector(lang);
  
  // 设置语言选择器下拉菜单显示/隐藏
  const languageSelector = document.getElementById('languageSelector');
  const languageDropdown = document.getElementById('languageDropdown');
  
  if (languageSelector && languageDropdown) {
    languageSelector.addEventListener('click', function(e) {
      e.stopPropagation();
      languageDropdown.classList.toggle('show');
    });
    
    document.addEventListener('click', function(e) {
      if (languageSelector && !languageSelector.contains(e.target)) {
        languageDropdown.classList.remove('show');
      }
    });
  }
  
  // 设置语言切换事件
  document.querySelectorAll('.language-option').forEach(option => {
    option.addEventListener('click', function() {
      const newLang = this.getAttribute('data-lang');
      setLanguage(newLang);
      
      // 隐藏下拉菜单
      if (languageDropdown) {
        languageDropdown.classList.remove('show');
      }
      
      // 添加视觉反馈
      this.classList.add('selected');
      setTimeout(() => {
        this.classList.remove('selected');
      }, 300);
    });
  });
}

// 导出函数供其他文件使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    translations,
    getCurrentLanguage,
    setLanguage,
    initLanguage
  };
}