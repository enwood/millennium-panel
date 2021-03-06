from django.db import models
from django.contrib.auth.models import Group
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
from millennium.panel.framehelpers import mmByte, mmWord, mmFlags, mmHextel

# Create your models here.

OnlyNumbersValidator = RegexValidator(
    r'^[0-9]*$',
    'Only 0-9 are allowed.',
    'Invalid Number'
)

ServiceCodeValidator = RegexValidator(
    r'^[125679][024][01234567]$',
    'Please enter a valid Service Code',
    'Invalid Service Code'
)

class FconfigOpts(models.Model):
    name = models.CharField(
        max_length=32,
    )
    tenant = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )
    terminal_type = models.CharField(
        choices=(
            ('00', 'Unknown Terminal Type'), # NULL_TERMINAL_TYPE
            ('01', 'Card Type Terminal'), # CARD_TERMINAL_TYPE
            ('02', 'Universal Type Terminal'), # UNIVERSAL_TERMINAL_TYPE
            ('03', 'Coin Terminal Type'), # COIN_TERMINAL_TYPE
            ('03', 'Maximim Terminal Type'), # MAXIMUM_TERMINAL_TYPE
            ('10', 'Smart Card Terminal Type'), # SMART_CARD_TERMINAL_TYPE
        ),
        default='02',
        max_length=2,
        verbose_name='Terminal Type',
    )
    display_present = models.BooleanField(
        default=True,
        verbose_name='Display present',
    )
    num_call_follow_on = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=5,
        null=True,
        blank=True,
        verbose_name='Number of Call follows',
    )
    card_validation_info = MultiSelectField(
        choices=(
            ('01', 'Auth for Local'), # DLOG_FCG_LOCAL_AUTH_REQ
            ('02', 'Delay Auth'), # DLOG_FCG_DELAY_AUTH
            ('04', 'MCE Auth for Local'), # DLOG_FCG_MCE_LOCAL_AUTH_REQ
            ('08', 'International'), # DLOG_FCG_VAL_INTL
            ('08', 'Insert NPA for 0+ Local/Intra'), # DLOG_FCG_INSERT_NPA_LOCAL
            ('10', 'Manually Entered Call Card'), # DLOG_FCG_MANUAL_CL_CARD
            ('00', 'ACCS Mode use NCC'), # DLOG_FCG_ACCS_MODE_NCC
            ('80', 'Validate after Number obtained'), # DLOG_FCG_MCE_VAL_AFTER_NUMBER
        ),
        default=['01', '04'],
        null=True,
        blank=True,
        verbose_name='Card validation info',
    )
    accs_info = MultiSelectField(
        choices=(
            ('01', 'ACCS Mode is available'), # DLOG_FCG_ACCS_AVAIL
            ('02', 'Route MCE Calls via 0+ network'), # DLOG_FCG_MCE_ROUTE_TO_ACCS
            ('04', 'MCE Feature enable'), # DLOG_FCG_ACCS_MCE_ENABLED
            ('08', 'MCE Calls MUST be NCC-validated'), # DLOG_FCG_ACCS_MCE_VAL_REQUIRED
            ('10', 'AOS Feature enable'), # DLOG_FCG_ACCS_AOS_ENABLED
            ('20', 'Strip off leading 0/1'), # DLOG_FCG_STRIP_OFF_0_OR_1
            ('80', 'Strip off local NPA'), # DLOG_FCG_STRIP_NPA_LOCAL
        ),
        default='01',
        null=True,
        blank=True,
        verbose_name='ACCS-Mode/Info',
    )
    incoming_call_mode = models.PositiveSmallIntegerField(
        choices=(
            (0, 'Ringing disabled'), # RINGING_DISABLED
            (1, 'Ringing / Incoming Voice'), # RINGING_INCOMING_VOICE
            (2, 'No Ringing / Data Call'), # NO_RINGING_DATA_CALL
            (3, 'Ringing / Voice / Delayed Data Call'), # RINGING_DELAYED_DATA_CALL
        ),
        default=1,
        verbose_name='Incoming Call mode',
    )
    incoming_call_anti_fraud = MultiSelectField(
        choices=(
            ('0', 'Answer Supervision'), # DLOG_FCG_ANS_SUPERVISN
        ),
        default='0',
        null=True,
        blank=True,
        verbose_name='Anti-Fraud for Incoming Call',
    )
    oos_pots_flags = MultiSelectField(
        choices=(
            ('01', 'Do not put Terminal Out-Of-Service when CDR list is full'), # CDR_FULL_NO_OOS
            ('02', 'Display Rate (MTR 1.x: Only Card-Terminals)'), # CARD_TERM_DISPLAY_RATE / TERM_DISPLAY_RATE
            ('04', 'INCOMMING_CALL_FCA_PRECED'), # INCOMMING_CALL_FCA_PRECED
            ('08', 'FCA_ZERO_VALUE_CARD'), # FCA_ZERO_VALUE_CARD
            ('10', 'MTR 1.x: Spare 4 / MTR 2.x: Automatically revert to primary Modem pool'), # SPARE_4 / REVERT_TO_PRIMARY_POOL
            ('20', 'MTR 1.x: Spare 5 / MTR 2.x: Block Carrier calls without nternal rate'), # SPARE_5 / BLOCK_NO_RATE_CARRIER
            ('40', 'MTR 1.x: Spare 6 / MTR 2.x: Creditcard CDRs should contain the charged amount for the calls'), # SPARE_6 / RATED_CREDIT_CARD_CDR
            ('80', 'MTR 1.x: Spare 7 / MTR 2.x: Force 11-digit-dialing on local calls'), # SPARE_7 / FORCE_11_DIGITS_LOCAL
        ),
        default=['01', '02', '04', '08'],
        null=True,
        blank=True,
        verbose_name='Out-Of-Service POTS Flags',
    )
    data_jack_visual_display = models.BooleanField(
        default=False,
        verbose_name='Datajack visual display',
    )

    incoming_call_rate = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=8,
        verbose_name='Incoming call rate',
        help_text='MTR1.x only'
    )
    language_scrolling_order = models.PositiveSmallIntegerField(
        choices=(
            (1, 'English'), # LANGUAGE_1
            (2, 'French'), # LANGUAGE_2
            (3, 'Spanish'), # LANGUAGE_3
            (4, 'Japanese'), # LANGUAGE_4
        ),
        default=1,
        verbose_name='Language Scrolling Order - 1st language',
        help_text='MTR 2.x only'
    )

    spareB = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Spare B',
        help_text='MTR1.x only'
    )
    language_scrolling_order_2 = models.PositiveSmallIntegerField(
        choices=(
            (1, 'English'), # LANGUAGE_1
            (2, 'French'), # LANGUAGE_2
            (3, 'Spanish'), # LANGUAGE_3
            (4, 'Japanese'), # LANGUAGE_4
        ),
        default=2,
        verbose_name='Language Scrolling Order - 2nd language',
        help_text='MTR 2.x only'
    )

    spareC = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Spare C',
        help_text='MTR1.x only'
    )
    number_of_languages = models.PositiveSmallIntegerField(
        choices=(
            (1, '1 Language'),
            (2, '2 Languages'),
            (3, '3 Languages (MTR 2.x only)'),
            (4, '4 Languages (MTR 2.x only)'),
        ),
        default=2,
        verbose_name='Number of Languages',
        help_text='MTR2.x only'
    )

    spareD = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Spare D',
        help_text='MTR1.x only'
    )
    rating_flags = MultiSelectField(
        choices=(
            ('01', 'Enable NPA SBR'), # NPA_SBR_ENABLE
            ('02', 'Enable International SBR'), # INTL_SBR_ENABLE
            #('03', ''), # INTL_SBR_FLAGS = (NPA_SBR_ENABLE|INTL_SBR_ENABLE)
            ('04', 'Enable Dial Around'), # DIAL_AROUND_ENABLED
            ('08', 'Show 1st xx min $, additional yy min $'), # SHOW_TIME_N_CHARGE
            ('10', 'Round up charge'), # SYSTEM_ROUND_UP
            ('20', '7-digit no-wait Option'), # SEVEN_DIGIT_NO_WAIT_ENABLE
        ),
        default=[],
        null=True,
        blank=True,
        verbose_name='Rating Flags',
        help_text='MTR2.x only'
    )

    spareE = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Spare E',
        help_text='MTR1.x only'
    )
    dial_around_timer = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Dial-around timer',
        help_text='MTR2.x only'
    )

    spareF = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Spare F',
        help_text='MTR1.x only'
    )
    opr_interntl_access_ptr = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Pointer to international Access Operator',
        help_text='MTR2.x only'
    )

    aos_number = models.CharField(
        max_length=12,
        validators=[
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='AOS number',
        help_text='MTR 1.x only'
    )
    aos_interlata_access = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Pointer to Inter-LATA AOS-number',
        help_text='MTR2.x only'
    )
    aos_interntl_access = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Pointer to International Access AOS-number',
        help_text='MTR2.x only'
    )
    djack_grace_before_collect = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Datajack grace-periode before collection',
        help_text='MTR2.x only'
    )
    opr_collection_tmr = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Operator collection timer	',
        help_text='MTR2.x only'
    )
    opr_intralata_access_ptr = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Pointer to Intra-LATA operator access number',
        help_text='MTR2.x only'
    )
    opr_interlata_access_ptr = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        null=True,
        blank=True,
        verbose_name='Pointer to Inter-LATA operator access number',
        help_text='MTR2.x only'
    )

    advert_enable = MultiSelectField(
        choices=(
            ('01', 'On Hook Adverts enabled'), # DLOG_FCG_ONHOOK_ADVERTS_ON
            ('02', 'Repdialer Adverts enabled'), # DLOG_FCG_REPDIALER_ADVERTS_ON
            ('04', 'Call Established adverts enabled'), # DLOG_FCG_CALL_EST_ADVERTS_ON
            #('06', 'Off Hook Adverts enabled'), # DLOG_FCG_OFFHOOK_ADVERTISING = (DLOG_FCG_REPDIALER_ADVERTS_ON | DLOG_FCG_CALL_EST_ADVERTS_ON)
            ('08', 'On Hook Date and Time displayed'), # DLOG_FCG_DATE_TIME_DISP_ON
            ('10', 'On Hook Date and Time displayed in 12hr Format'), # DLOG_FCG_DATE_TIME_DISP_12HR
        ),
        default=['01'],
        null=True,
        blank=True,
        verbose_name='Enable Advertising',
    )
    default_language = models.PositiveSmallIntegerField(
        choices=(
            (0, 'English'), # LANGUAGE_1
            (1, 'French'), # LANGUAGE_2
            (2, 'Spanish'), # LANGUAGE_3
            (3, 'Japanese'), # LANGUAGE_4
        ),
        default=1,
        verbose_name='Default Language',
    )

    display_called_number = MultiSelectField(
        choices=(
            ('01', 'Display Called Number Prompt'), # DLOG_FCG_DISPLAY_CALLED_NUM_PROMPT
            ('80', 'Surpress Calling Prompt'), # DLOG_FCG_SUPPRESS_CALLING_PROMPT
        ),
        default=['01'],
        null=True,
        blank=True,
        verbose_name='Called Number Displaying',
    )
    dtmf_duration = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=8,
        verbose_name='DTMF Duration',
    )
    inter_digit_pause = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=8,
        verbose_name='Inter-digit Pause',
    )

    dialing_conversion = MultiSelectField(
        choices=(
            ('01', 'Convert Operator to Toll'), # DLOG_FCG_DCV_OP_TO_TOLL
            ('02', 'Convert Toll to Operator'), # DLOG_FCG_DCV_TOLL_TO_OP
        ),
        default=['01', '02'],
        null=True,
        blank=True,
        verbose_name='Incoming Call mode',
        help_text='MTR 1.x only',
    )
    ppu_pre_auth_credit_limit = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='PPU PreAuth Credit Limit',
        help_text='MTR 2.x only',
    )

    coin_call_features = MultiSelectField(
        choices=(
            ('01', 'Overtime'), # DLOG_FCG_COIN_OVERTIME
            ('02', 'Voice-Feedback'), # DLOG_FCG_COIN_VFDBCK
            ('04', '2nd Warning'), # DLOG_FCG_COIN_2ND_WARN
        ),
        default=['02', '04'],
        null=True,
        blank=True,
        verbose_name='Coin calling Features',
    )
    coin_call_overtime_period = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=5,
        verbose_name='Coin call overtime period',
    )
    coin_call_pots_time = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=120,
        verbose_name='Coin call POTS time',
    )
    min_international_digits = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=5,
        verbose_name='Minimum number of digits for international calls',
    )
    def_rate_req_payment = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=10,
        verbose_name='default rate request payment type',
    )
    next_call_revalidation_freq = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Next Call re-validation frequency',
    )
    cutoff_on_disconnect_duration = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=45,
        verbose_name='Cutoff on disconnect duration',
    )
    cdr_upload_timer_int = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=0,
        verbose_name='CDR Upload timer for international calls',
    )
    cdr_upload_timer_nonint = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=0,
        verbose_name='CDR Upload timer for non-international calls',
    )
    perf_stats_dialog_fails = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Number of performance statistics dialog fails',
    )
    co_line_check_fails = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Number of CO-line-check fails',
    )
    alt_ncc_dialog_fails = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Number of alternative NCC-dialog-check fails',
    )
    dialog_fails_till_oos = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Number of failed dialogues until Terminal goes Out-Of-Service',
    )
    dialog_fails_till_alarm = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Number of failed dialogues until alarm is sent',
    )
    smart_card_flags = MultiSelectField(
        choices=(
            ('20', 'POST_PAYMENT_RATE_REQUEST'), # POST_PAYMENT_RATE_REQUEST
            ('80', 'DLOG_FCG_SUPPRESS_TERMINAL_RATE_INFO'), # DLOG_FCG_SUPPRESS_TERMINAL_RATE_INFO
        ),
        default=['01'],
        null=True,
        blank=True,
        verbose_name='Smartcard Flags',
    )
    max_man_card_dig = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=14,
        verbose_name='Maximum number of digits of manual card entry',
    )
    aos_intra_access_ptr = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Pointer to Intra-AOS access-number',
    )
    carrier_reroute_flags = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Carrier reroute-flags',
    )
    min_man_card_dig = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=14,
        verbose_name='Minimum number of digits of manual card entry',
    )
    max_smart_card_inserts = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=5,
        verbose_name='Maximum number of smartcard-inserts',
    )
    max_diff_smart_card_inserts = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=5,
        verbose_name='Maximum number of different smartcard-inserts',
    )
    aos_operator_access_ptr = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Pointer to Operator AOS-number',
    )
    data_jack_flags = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Datajack-flag',
    )
    onhook_alarm_delay = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=500,
        verbose_name='Delay for on-hook card alarm delay',
    )
    post_onhook_alarm_delay = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=100,
        verbose_name='Delay for on-hook card alarm delay after call',
    )
    card_alarm_duration = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=1000,
        verbose_name='Duration of card-alarm',
    )
    alarm_cadence_on_timer = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=50,
        verbose_name='Card-alarm On-cadence',
    )
    alarm_cadence_off_timer = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=50,
        verbose_name='Card-alarm Off-cadence',
    )
    cardrdr_blocked_alarm_delay = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535),
            OnlyNumbersValidator
        ],
        default=300,
        verbose_name='Delay until card-reader blocked Alarm',
    )
    settle_time = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=8,
        verbose_name='Settlement time',
    )
    grace_period_domestic = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=5,
        verbose_name='Grace period for domestic calls',
    )
    ias_timeout = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=90,
        verbose_name='IAS timeout',
    )
    grace_period_international = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Grace period for international calls',
    )
    settle_time_datajack = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(255),
            OnlyNumbersValidator,
        ],
        default=0,
        verbose_name='Settlement-time for datajack-calls',
    )

    def __str__(self):
        return self.name

    def getFrame(self, MTRconfig):
        outframe = [0x1A]
        outframe.extend(mmByte(self.terminal_type))
        outframe.extend(mmByte(self.display_present))
        outframe.extend(mmByte(self.num_call_follow_on))
        outframe.extend(mmFlags(self.card_validation_info))
        outframe.extend(mmFlags(self.accs_info))
        outframe.extend(mmByte(self.incoming_call_mode))
        outframe.extend(mmFlags(self.incoming_call_anti_fraud))
        outframe.extend(mmFlags(self.oos_pots_flags))
        outframe.extend(mmByte(self.data_jack_visual_display))

        if MTRconfig['MTR'] is 1:
            outframe.extend(mmByte(self.incoming_call_rate))
            outframe.extend(mmByte(self.spareB))
            outframe.extend(mmByte(self.spareC))
            outframe.extend(mmByte(self.spareD))
            outframe.extend(mmByte(self.spareE))
            outframe.extend(mmByte(self.spareF))
            outframe.extend(mmHextel(self.aos_number, MTRconfig['NA_LDIST_TEL_NUM_LEN']))
        elif MTRconfig['MTR'] is 2:
            outframe.extend(mmByte(self.language_scrolling_order))
            outframe.extend(mmByte(self.language_scrolling_order_2))
            outframe.extend(mmByte(self.number_of_languages))
            outframe.extend(mmFlags(self.rating_flags))
            outframe.extend(mmByte(self.dial_around_timer))
            outframe.extend(mmByte(self.opr_interntl_access_ptr))
            outframe.extend(mmByte(self.aos_interlata_access))
            outframe.extend(mmByte(self.aos_interntl_access))
            outframe.extend(mmByte(self.djack_grace_before_collect))
            outframe.extend(mmByte(self.opr_collection_tmr))
            outframe.extend(mmByte(self.opr_intralata_access_ptr))
            outframe.extend(mmByte(self.opr_interlata_access_ptr))

        outframe.extend(mmFlags(self.advert_enable))
        outframe.extend(mmByte(self.default_language))
        outframe.extend(mmFlags(self.display_called_number))
        outframe.extend(mmByte(self.dtmf_duration))
        outframe.extend(mmByte(self.inter_digit_pause))

        if MTRconfig['MTR'] is 1:
            outframe.extend(mmFlags(self.dialing_conversion))
        elif MTRconfig['MTR'] is 2:
            outframe.extend(mmByte(self.ppu_pre_auth_credit_limit))

        outframe.extend(mmFlags(self.coin_call_features))
        outframe.extend(mmWord(self.coin_call_overtime_period))
        outframe.extend(mmWord(self.coin_call_pots_time))
        outframe.extend(mmByte(self.min_international_digits))
        outframe.extend(mmByte(self.def_rate_req_payment))
        outframe.extend(mmByte(self.next_call_revalidation_freq))
        outframe.extend(mmByte(self.cutoff_on_disconnect_duration))
        outframe.extend(mmWord(self.cdr_upload_timer_int))
        outframe.extend(mmWord(self.cdr_upload_timer_nonint))
        outframe.extend(mmByte(self.perf_stats_dialog_fails))
        outframe.extend(mmByte(self.co_line_check_fails))
        outframe.extend(mmByte(self.alt_ncc_dialog_fails))
        outframe.extend(mmByte(self.dialog_fails_till_oos))
        outframe.extend(mmByte(self.dialog_fails_till_alarm))
        outframe.extend(mmFlags(self.smart_card_flags))
        outframe.extend(mmByte(self.max_man_card_dig))
        outframe.extend(mmByte(self.aos_intra_access_ptr))
        outframe.extend(mmByte(self.carrier_reroute_flags))
        outframe.extend(mmByte(self.min_man_card_dig))
        outframe.extend(mmByte(self.max_smart_card_inserts))
        outframe.extend(mmByte(self.max_diff_smart_card_inserts))
        outframe.extend(mmByte(self.aos_operator_access_ptr))
        outframe.extend(mmByte(self.data_jack_flags))
        outframe.extend(mmWord(self.onhook_alarm_delay))
        outframe.extend(mmWord(self.post_onhook_alarm_delay))
        outframe.extend(mmWord(self.card_alarm_duration))
        outframe.extend(mmWord(self.alarm_cadence_on_timer))
        outframe.extend(mmWord(self.alarm_cadence_off_timer))
        outframe.extend(mmWord(self.cardrdr_blocked_alarm_delay))
        outframe.extend(mmByte(self.settle_time))
        outframe.extend(mmByte(self.grace_period_domestic))
        outframe.extend(mmByte(self.ias_timeout))
        outframe.extend(mmByte(self.grace_period_international))
        outframe.extend(mmByte(self.settle_time_datajack))

        return(outframe)


    class Meta:
        unique_together = (('name', 'tenant'),)
        verbose_name = 'Feature Config & Call Options'
        verbose_name_plural = 'Feature Config & Call Options'
