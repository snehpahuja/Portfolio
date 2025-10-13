import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Set page config
st.set_page_config(page_title="NGO Student Analytics Dashboard", layout="wide")

# Load data
# upay_app/centre_analysis.py

@st.cache_data
def load_data():
    # The paths are relative to the project root where you run the streamlit command
    att = pd.read_csv("data/attendance.csv", parse_dates=['date'])
    grd = pd.read_csv("data/grades.csv", parse_dates=['date'])
    diary = pd.read_csv("data/center_diary.csv", parse_dates=['date'])

    centre_progress = {
        'center_info': pd.read_csv("data/center_info.csv"),
        'expenses': pd.read_csv("data/expenses.csv", parse_dates=['date']),
        'volunteers': pd.read_csv("data/volunteers.csv", parse_dates=['date']),
        'visitors': pd.read_csv("data/visitors.csv", parse_dates=['date']),
        'activities': pd.read_csv("data/activities.csv", parse_dates=['date']),
        'problems': pd.read_csv("data/problems.csv", parse_dates=['date']),
        'requirements': pd.read_csv("data/requirements.csv")
    }

    return att, grd, diary, centre_progress

df_attendance, df_grades, df_diary, centre_data = load_data()

# -------------------------
# Sidebar navigation
# -------------------------
st.sidebar.title("Navigation")
dashboard_type = st.sidebar.radio(
    "Select Dashboard:",
    ["General Attendance Overview", "Student Profile", "Centre Progress Dashboard"],
    index=0
)

# -------------------------
# General Attendance Overview (unchanged logic)
# -------------------------
if dashboard_type == "General Attendance Overview":
    # --- (use original code from your app; shortened here for brevity) ---
    st.sidebar.markdown("---")
    st.sidebar.header("PRIMARY VIEW")
    view_type = st.sidebar.radio(
        "Show attendance for:",
        ["All Centers (Overall)", "Specific City", "Specific Center", "Individual Student"],
        index=0
    )

    primary_filter = {}

    if view_type == "Specific City":
        cities = sorted(df_attendance['city'].unique())
        selected_city = st.sidebar.selectbox("Select City:", cities)
        primary_filter['city'] = selected_city
        primary_label = f"{selected_city} Average"

    elif view_type == "Specific Center":
        centers = sorted(df_attendance['center'].unique())
        selected_center = st.sidebar.selectbox("Select Center:", centers)
        primary_filter['center'] = selected_center
        primary_label = selected_center

    elif view_type == "Individual Student":
        students = sorted(df_attendance['student_name'].unique())
        selected_student = st.sidebar.selectbox("Select Student:", students)
        primary_filter['student_name'] = selected_student
        primary_label = selected_student
    else:
        primary_label = "Overall Average"

    # Comparison Section
    st.sidebar.markdown("---")
    st.sidebar.header("ADD COMPARISON")
    enable_comparison = st.sidebar.checkbox("Enable Comparison Mode")

    comparison_items = []
    if enable_comparison:
        st.sidebar.info("Select 2-4 items to compare")

        comparison_type = st.sidebar.selectbox(
            "Compare by:",
            ["Centers", "Cities", "Grades", "Students"]
        )

        if comparison_type == "Centers":
            available_centers = sorted(df_attendance['center'].unique())
            comparison_items = st.sidebar.multiselect(
                "Select Centers:",
                available_centers,
                max_selections=4
            )
        elif comparison_type == "Cities":
            available_cities = sorted(df_attendance['city'].unique())
            comparison_items = st.sidebar.multiselect(
                "Select Cities:",
                available_cities,
                max_selections=4
            )
        elif comparison_type == "Grades":
            available_grades = sorted(df_attendance['grade'].unique())
            comparison_items = st.sidebar.multiselect(
                "Select Grades:",
                available_grades,
                max_selections=4
            )
        else:  # Students
            available_students = sorted(df_attendance['student_name'].unique())
            comparison_items = st.sidebar.multiselect(
                "Select Students:",
                available_students,
                max_selections=4
            )

    # Time Period Filter
    st.sidebar.markdown("---")
    st.sidebar.header("TIME PERIOD")
    time_range = st.sidebar.selectbox(
        "Select Period:",
        ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last 12 Months", "This Year", "All Time", "Custom Range"]
    )

    time_granularity = st.sidebar.radio(
        "View by:",
        ["Daily", "Weekly", "Monthly", "Yearly"],
        index=2
    )

    granularity_map = {
        "Daily": "D",
        "Weekly": "W",
        "Monthly": "ME",
        "Yearly": "YE"
    }

    # Filter data by time range
    end_date = df_attendance['date'].max()
    if time_range == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
    elif time_range == "Last 3 Months":
        start_date = end_date - timedelta(days=90)
    elif time_range == "Last 6 Months":
        start_date = end_date - timedelta(days=180)
    elif time_range == "Last 12 Months":
        start_date = end_date - timedelta(days=365)
    elif time_range == "This Year":
        start_date = datetime(end_date.year, 1, 1)
    elif time_range == "Custom Range":
        col1, col2 = st.sidebar.columns(2)
        start_date = col1.date_input("From:", value=end_date - timedelta(days=90))
        end_date = col2.date_input("To:", value=end_date)
    else:
        start_date = df_attendance['date'].min()

    st.title("General Attendance Overview")

    df_filtered = df_attendance[(df_attendance['date'] >= pd.Timestamp(start_date)) &
                                (df_attendance['date'] <= pd.Timestamp(end_date))]

    # Calculate attendance
    def calc_attendance(filtered_df, time_gran):
        attendance = filtered_df.groupby(pd.Grouper(key='date', freq=time_gran)).agg({
            'present': ['sum', 'count']
        }).reset_index()
        attendance.columns = ['date', 'present_count', 'total_count']
        attendance['percentage'] = (attendance['present_count'] / attendance['total_count'] * 100).round(2)
        return attendance

    # Primary data
    if primary_filter:
        primary_df = df_filtered.copy()
        for key, value in primary_filter.items():
            primary_df = primary_df[primary_df[key] == value]
    else:
        primary_df = df_filtered.copy()

    primary_attendance = calc_attendance(primary_df, granularity_map[time_granularity])

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    overall_attendance = (primary_df['present'].sum() / len(primary_df) * 100) if len(primary_df) > 0 else 0
    total_students = primary_df['student_name'].nunique()
    at_risk_students = primary_df.groupby('student_name')['present'].mean()
    at_risk_count = (at_risk_students < 0.75).sum()

    prev_start = start_date - (end_date - start_date)
    df_prev = df_attendance[(df_attendance['date'] >= pd.Timestamp(prev_start)) &
                            (df_attendance['date'] < pd.Timestamp(start_date))]
    prev_attendance = (df_prev['present'].sum() / len(df_prev) * 100) if len(df_prev) > 0 else 0
    trend = overall_attendance - prev_attendance

    with col1:
        st.metric("Overall Attendance", f"{overall_attendance:.1f}%", f"{trend:+.1f}%")
    with col2:
        st.metric("Total Students", total_students)
    with col3:
        st.metric("At-Risk (<75%)", at_risk_count, delta_color="inverse")
    with col4:
        st.metric("Period", f"{time_granularity}")

    # Line graph
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=primary_attendance['date'],
        y=primary_attendance['percentage'],
        mode='lines+markers',
        name=primary_label,
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))

    if enable_comparison and comparison_items:
        colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

        for idx, item in enumerate(comparison_items):
            comp_df = df_filtered.copy()

            if comparison_type == "Centers":
                comp_df = comp_df[comp_df['center'] == item]
            elif comparison_type == "Cities":
                comp_df = comp_df[comp_df['city'] == item]
            elif comparison_type == "Grades":
                comp_df = comp_df[comp_df['grade'] == item]
            else:
                comp_df = comp_df[comp_df['student_name'] == item]

            comp_attendance = calc_attendance(comp_df, granularity_map[time_granularity])

            fig.add_trace(go.Scatter(
                x=comp_attendance['date'],
                y=comp_attendance['percentage'],
                mode='lines+markers',
                name=f"{item}",
                line=dict(color=colors[idx % len(colors)], width=2),
                marker=dict(size=6)
            ))

    graph_title = f"Attendance Trends: {primary_label}"
    if enable_comparison and comparison_items:
        graph_title += f" vs {', '.join(comparison_items)}"

    fig.update_layout(
        title=graph_title,
        xaxis_title="Date",
        yaxis_title="Attendance Percentage (%)",
        hovermode='x unified',
        height=500,
        yaxis=dict(range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Bottom section
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("At-Risk Students (<75% Attendance)")

        student_attendance = primary_df.groupby(['student_name', 'center', 'grade']).agg({
            'present': ['sum', 'count']
        }).reset_index()
        student_attendance.columns = ['student_name', 'center', 'grade', 'present_count', 'total_count']
        student_attendance['percentage'] = (student_attendance['present_count'] / student_attendance['total_count'] * 100).round(1)

        at_risk_df = student_attendance[student_attendance['percentage'] < 75].sort_values('percentage')

        if len(at_risk_df) > 0:
            at_risk_df['Status'] = at_risk_df['percentage'].apply(
                lambda x: 'Critical' if x < 70 else 'At-Risk'
            )

            display_df = at_risk_df[['student_name', 'center', 'grade', 'percentage', 'Status']]
            display_df.columns = ['Student Name', 'Center', 'Grade', 'Attendance %', 'Status']

            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.success("No students below 75% attendance threshold!")

    with col2:
        st.subheader("Center Performance Comparison")

        center_attendance = df_filtered.groupby('center').agg({
            'present': ['sum', 'count']
        }).reset_index()
        center_attendance.columns = ['center', 'present_count', 'total_count']
        center_attendance['percentage'] = (center_attendance['present_count'] / center_attendance['total_count'] * 100).round(1)
        center_attendance = center_attendance.sort_values('percentage', ascending=True)

        fig_centers = go.Figure(go.Bar(
            x=center_attendance['percentage'],
            y=center_attendance['center'],
            orientation='h',
            marker=dict(
                color=center_attendance['percentage'],
                colorscale=[[0, '#d62728'], [0.75, '#ff7f0e'], [0.9, '#2ca02c'], [1, '#2ca02c']],
                showscale=False
            ),
            text=center_attendance['percentage'].apply(lambda x: f"{x:.1f}%"),
            textposition='outside'
        ))

        fig_centers.update_layout(
            xaxis_title="Attendance Percentage (%)",
            yaxis_title="",
            height=400,
            xaxis=dict(range=[0, 100])
        )

        st.plotly_chart(fig_centers, use_container_width=True)

    st.markdown("---")
    st.info("Tip: Enable Comparison Mode to compare attendance across multiple centers, cities, grades, or students.")

# -------------------------
# Student Profile Dashboard 
# -------------------------
elif dashboard_type == "Student Profile":
    st.title("Student Profile Dashboard")

    st.sidebar.markdown("---")
    st.sidebar.header("SELECT STUDENT")

    students = sorted(df_grades['student_name'].unique())
    selected_student = st.sidebar.selectbox("Student Name:", students)

    # Get student info
    student_info = df_grades[df_grades['student_name'] == selected_student].iloc[0]

    st.sidebar.markdown("---")
    st.sidebar.header("TIME PERIOD")

    profile_time_range = st.sidebar.selectbox(
        "Select Period:",
        ["Last 3 Months", "Last 6 Months", "This Year", "All Time", "Custom Range"],
        key="profile_time"
    )

    profile_end_date = df_grades['date'].max()
    if profile_time_range == "Last 3 Months":
        profile_start_date = profile_end_date - timedelta(days=90)
    elif profile_time_range == "Last 6 Months":
        profile_start_date = profile_end_date - timedelta(days=180)
    elif profile_time_range == "This Year":
        profile_start_date = datetime(profile_end_date.year, 1, 1)
    elif profile_time_range == "Custom Range":
        col1, col2 = st.sidebar.columns(2)
        profile_start_date = col1.date_input("From:", value=profile_end_date - timedelta(days=90), key="profile_start")
        profile_end_date = col2.date_input("To:", value=profile_end_date, key="profile_end")
    else:
        profile_start_date = df_grades['date'].min()

    # Student profile header
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Student", selected_student)
    with col2:
        st.metric("Grade", student_info['grade'])
    with col3:
        st.metric("Center", student_info['center'])
    with col4:
        st.metric("City", student_info['city'])

    st.markdown("---")

    # ========== ATTENDANCE SECTION ==========
    st.header("Attendance Overview")

    # Filter attendance data for student
    student_attendance_data = df_attendance[
        (df_attendance['student_name'] == selected_student) &
        (df_attendance['date'] >= pd.Timestamp(profile_start_date)) &
        (df_attendance['date'] <= pd.Timestamp(profile_end_date))
    ]

    # Calculate attendance metrics
    total_days = len(student_attendance_data)
    days_present = student_attendance_data['present'].sum()
    attendance_pct = (days_present / total_days * 100) if total_days > 0 else 0

    # Monthly attendance trend
    monthly_attendance = student_attendance_data.groupby(pd.Grouper(key='date', freq='ME')).agg({
        'present': ['sum', 'count']
    }).reset_index()
    monthly_attendance.columns = ['date', 'present_count', 'total_count']
    monthly_attendance['percentage'] = (monthly_attendance['present_count'] / monthly_attendance['total_count'] * 100).round(2)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Attendance", f"{attendance_pct:.1f}%")
    with col2:
        st.metric("Days Present", f"{int(days_present)}/{total_days}")
    with col3:
        status = "Good" if attendance_pct >= 85 else "Average" if attendance_pct >= 75 else "At Risk"
        st.metric("Status", status)

    # Attendance line chart
    fig_att = go.Figure()

    fig_att.add_trace(go.Scatter(
        x=monthly_attendance['date'],
        y=monthly_attendance['percentage'],
        mode='lines+markers',
        name='Attendance',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.2)'
    ))

    fig_att.update_layout(
        title=f"Attendance Trend for {selected_student}",
        xaxis_title="Month",
        yaxis_title="Attendance Percentage (%)",
        height=400,
        yaxis=dict(range=[0, 100]),
        hovermode='x'
    )

    st.plotly_chart(fig_att, use_container_width=True)

    st.markdown("---")

    # ========== GRADES SECTION ==========
    st.header("Academic Performance")

    # Subject selection
    all_subjects = sorted(df_grades['subject'].unique())
    selected_subjects = st.multiselect(
        "Select Subjects to Display:",
        all_subjects,
        default=all_subjects[:5],
        key="subject_select"
    )

    if not selected_subjects:
        st.warning("Please select at least one subject to display.")
    else:
        # Filter grades data
        student_grades_data = df_grades[
            (df_grades['student_name'] == selected_student) &
            (df_grades['date'] >= pd.Timestamp(profile_start_date)) &
            (df_grades['date'] <= pd.Timestamp(profile_end_date))
        ]

        student_data_filtered = student_grades_data[student_grades_data['subject'].isin(selected_subjects)].copy()
        student_data_filtered['percentage'] = (student_data_filtered['marks'] / student_data_filtered['max_marks'] * 100).round(1)

        # Grades line chart
        fig_grades = go.Figure()

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

        for idx, subject in enumerate(selected_subjects):
            subject_data = student_data_filtered[student_data_filtered['subject'] == subject]

            fig_grades.add_trace(go.Scatter(
                x=subject_data['date'],
                y=subject_data['percentage'],
                mode='lines+markers',
                name=subject,
                line=dict(color=colors[idx % len(colors)], width=2),
                marker=dict(size=8)
            ))

        fig_grades.update_layout(
            title=f"Performance Trends - {selected_student}",
            xaxis_title="Date",
            yaxis_title="Score (%)",
            hovermode='x unified',
            height=450,
            yaxis=dict(range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig_grades, use_container_width=True)

        # Performance details
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Current Performance")

            latest_scores = student_data_filtered.sort_values('date').groupby('subject').last().reset_index()
            latest_scores = latest_scores[['subject', 'marks', 'max_marks', 'percentage']].sort_values('percentage', ascending=False)

            def get_category(pct):
                if pct >= 80:
                    return "Excellent"
                elif pct >= 60:
                    return "Good"
                elif pct >= 40:
                    return "Average"
                else:
                    return "Needs Improvement"

            latest_scores['Performance'] = latest_scores['percentage'].apply(get_category)
            latest_scores['Score'] = latest_scores.apply(lambda x: f"{int(x['marks'])}/{int(x['max_marks'])}", axis=1)

            display_latest = latest_scores[['subject', 'Score', 'percentage', 'Performance']]
            display_latest.columns = ['Subject', 'Score', '%', 'Performance']

            st.dataframe(display_latest, use_container_width=True, hide_index=True)

        with col2:
            st.subheader("Performance Trends")

            trend_data = []
            for subject in selected_subjects:
                subj_data = student_data_filtered[student_data_filtered['subject'] == subject].sort_values('date')
                if len(subj_data) >= 2:
                    mid_point = len(subj_data) // 2
                    first_half_avg = subj_data.iloc[:mid_point]['percentage'].mean()
                    second_half_avg = subj_data.iloc[mid_point:]['percentage'].mean()
                    trend = second_half_avg - first_half_avg

                    if trend > 5:
                        trend_str = "Improving"
                    elif trend < -5:
                        trend_str = "Declining"
                    else:
                        trend_str = "Stable"

                    trend_data.append({
                        'Subject': subject,
                        'Current': f"{second_half_avg:.1f}%",
                        'Change': f"{trend:+.1f}%",
                        'Trend': trend_str
                    })

            if trend_data:
                trend_df = pd.DataFrame(trend_data)
                st.dataframe(trend_df, use_container_width=True, hide_index=True)
            else:
                st.info("Not enough data to show trends")

        # Overall statistics
        st.markdown("---")
        st.subheader("Overall Academic Statistics")

        col1, col2, col3, col4 = st.columns(4)

        overall_avg = student_data_filtered['percentage'].mean()
        highest_score = student_data_filtered['percentage'].max()
        lowest_score = student_data_filtered['percentage'].min()
        total_assessments = len(student_data_filtered)

        with col1:
            st.metric("Overall Average", f"{overall_avg:.1f}%")
        with col2:
            st.metric("Highest Score", f"{highest_score:.1f}%")
        with col3:
            st.metric("Lowest Score", f"{lowest_score:.1f}%")
        with col4:
            st.metric("Total Assessments", total_assessments)

    st.markdown("---")
    st.info("Tip: This profile shows both attendance and academic performance for the selected student in separate sections.")

# -------------------------
# Centre Progress Dashboard
# -------------------------
else:
    st.title("Centre Progress Dashboard")

    # Top filters area
    st.sidebar.markdown("---")
    st.sidebar.header("CENTRE FILTERS")

    center_info = centre_data['center_info']
    centers = center_info['center'].tolist()
    cities = sorted(center_info['city'].unique())

    selected_city = st.sidebar.selectbox("City / Zone:", ["All"] + cities)
    selected_center = st.sidebar.selectbox("Centre:", ["All"] + centers)

    date_filter = st.sidebar.selectbox("Date Range:", ["Last 3 Months", "Last 6 Months", "This Year", "All Time", "Custom Range"])
    end_date = centre_data['expenses']['date'].max()
    if date_filter == "Last 3 Months":
        start_date = end_date - timedelta(days=90)
    elif date_filter == "Last 6 Months":
        start_date = end_date - timedelta(days=180)
    elif date_filter == "This Year":
        start_date = datetime(end_date.year, 1, 1)
    elif date_filter == "Custom Range":
        col1, col2 = st.sidebar.columns(2)
        start_date = pd.to_datetime(col1.date_input("From:", value=end_date - timedelta(days=90)))
        end_date = pd.to_datetime(col2.date_input("To:", value=end_date))
    else:
        start_date = centre_data['expenses']['date'].min()

    # Filter function
    def filter_by_selection(df, center_col='center'):
        df2 = df.copy()
        if selected_city != "All":
            df2 = df2.merge(center_info[['center', 'city']], on='center', how='left')
            df2 = df2[df2['city'] == selected_city]
        if selected_center != "All":
            df2 = df2[df2['center'] == selected_center]
        df2 = df2[(df2['date'] >= pd.Timestamp(start_date)) & (df2['date'] <= pd.Timestamp(end_date))]
        return df2

    # KPIs top row
    st.markdown("### Key KPIs")
    exp_filtered = filter_by_selection(centre_data['expenses'])
    vol_filtered = filter_by_selection(centre_data['volunteers'])
    vis_filtered = filter_by_selection(centre_data['visitors'])
    act_filtered = filter_by_selection(centre_data['activities'])

    # Derive simple KPIs
    total_students_est = df_attendance[df_attendance['date'].between(start_date, end_date)]
    if selected_center != "All":
        total_students_est = total_students_est[total_students_est['center'] == selected_center]
    elif selected_city != "All":
        total_students_est = total_students_est.merge(center_info[['center', 'city']], on='center', how='left')
        total_students_est = total_students_est[total_students_est['city'] == selected_city]

    total_students_cnt = total_students_est['student_name'].nunique()
    avg_attendance_pct = (total_students_est['present'].sum() / len(total_students_est) * 100) if len(total_students_est) > 0 else 0
    total_volunteers = vol_filtered['name'].nunique()
    total_visitors = vis_filtered['name'].nunique()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students (est.)", total_students_cnt)
    c2.metric("Avg Attendance", f"{avg_attendance_pct:.1f}%")
    c3.metric("Volunteers", total_volunteers)
    c4.metric("Visitors", total_visitors)

    st.markdown("---")

    # Centre-wise breakdown table
    st.subheader("Centre-wise Breakdown")
    # Aggregate activities + attendance approximations per center
    # Use activities dataframe for classes and percentages
    act_agg = act_filtered.groupby('center').agg({
        'classes': 'sum',
        'homework_done_pct': 'mean',
        'pt_done_pct': 'mean',
        'prayer_done_pct': 'mean',
        'extra_activity_pct': 'mean'
    }).reset_index()

    # attendance per centre in the date range
    att_filtered = df_attendance[(df_attendance['date'] >= pd.Timestamp(start_date)) & (df_attendance['date'] <= pd.Timestamp(end_date))]
    if selected_center != "All":
        att_filtered = att_filtered[att_filtered['center'] == selected_center]
    if selected_city != "All":
        att_filtered = att_filtered.merge(center_info[['center', 'city']], on='center', how='left')
        att_filtered = att_filtered[att_filtered['city'] == selected_city]

    att_agg = att_filtered.groupby('center').agg({'present': ['sum', 'count']})
    if not att_agg.empty:
        att_agg.columns = ['present_count', 'total_count']
        att_agg = att_agg.reset_index()
        att_agg['attendance_pct'] = (att_agg['present_count'] / att_agg['total_count'] * 100).round(1)
    else:
        att_agg = pd.DataFrame(columns=['center', 'present_count', 'total_count', 'attendance_pct'])

    centre_breakdown = act_agg.merge(att_agg, on='center', how='left').fillna(0)
    centre_breakdown = centre_breakdown.merge(center_info[['center', 'city']], on='center', how='left')
    centre_breakdown = centre_breakdown[['center', 'city', 'classes', 'attendance_pct', 'homework_done_pct', 'pt_done_pct', 'prayer_done_pct', 'extra_activity_pct']]
    centre_breakdown.columns = ['Center', 'City', 'Classes (sum)', 'Attendance %', 'Homework %', 'PT %', 'Prayer %', 'Extra Activity %']

    st.dataframe(centre_breakdown.sort_values('Attendance %', ascending=False), use_container_width=True)

    st.markdown("---")

    # Expenditure Section
    st.subheader("Expenditure Trend")
    if exp_filtered.empty:
        st.info("No expense data for the selected filters/date range.")
    else:
        exp_monthly = exp_filtered.groupby(pd.Grouper(key='date', freq='M')).agg({'amount': 'sum'}).reset_index()
        fig_exp = go.Figure()
        fig_exp.add_trace(go.Scatter(
            x=exp_monthly['date'],
            y=exp_monthly['amount'],
            mode='lines+markers',
            name='Expenditure',
            line=dict(width=3),
            marker=dict(size=8)
        ))
        fig_exp.update_layout(title="Monthly Expenditure", xaxis_title="Month", yaxis_title="Amount", height=350)
        st.plotly_chart(fig_exp, use_container_width=True)

        st.markdown("**Expense Details**")
        exp_by_type = exp_filtered.groupby(['type']).agg({'amount': 'sum'}).reset_index().sort_values('amount', ascending=False)
        st.dataframe(exp_by_type, use_container_width=True)

    st.markdown("---")

    # Volunteers & Visitors side-by-side
    st.subheader("Volunteers & Visitors")

    vcol1, vcol2 = st.columns(2)
    with vcol1:
        st.markdown("**Volunteers (recent logs)**")
        if vol_filtered.empty:
            st.info("No volunteers recorded.")
        else:
            recent_vols = vol_filtered.sort_values('date', ascending=False).head(20)
            st.dataframe(recent_vols[['date', 'center', 'name', 'hours', 'subject']].sort_values('date', ascending=False), use_container_width=True)

            # Volunteers over time
            vols_time = vol_filtered.groupby(pd.Grouper(key='date', freq='M')).agg({'name': 'nunique'}).reset_index()
            vols_time.columns = ['date', 'unique_volunteers']
            fig_vol_time = go.Figure(go.Bar(x=vols_time['date'], y=vols_time['unique_volunteers']))
            fig_vol_time.update_layout(title="Unique Volunteers per Month", xaxis_title="Month", yaxis_title="Volunteers", height=300)
            st.plotly_chart(fig_vol_time, use_container_width=True)

    with vcol2:
        st.markdown("**Visitors (recent logs)**")
        if vis_filtered.empty:
            st.info("No visitors recorded.")
        else:
            recent_vis = vis_filtered.sort_values('date', ascending=False).head(20)
            st.dataframe(recent_vis[['date', 'center', 'name', 'type', 'purpose']].sort_values('date', ascending=False), use_container_width=True)

            vis_time = vis_filtered.groupby(pd.Grouper(key='date', freq='M')).agg({'name': 'nunique'}).reset_index()
            vis_time.columns = ['date', 'unique_visitors']
            fig_vis_time = go.Figure(go.Bar(x=vis_time['date'], y=vis_time['unique_visitors']))
            fig_vis_time.update_layout(title="Unique Visitors per Month", xaxis_title="Month", yaxis_title="Visitors", height=300)
            st.plotly_chart(fig_vis_time, use_container_width=True)

    st.markdown("---")

    # Problems / Requirements
    st.subheader("Problems & Requirements")
    prob_filtered = centre_data['problems']
    req_filtered = centre_data['requirements']
    if selected_center != "All":
        prob_filtered = prob_filtered[prob_filtered['center'] == selected_center]
        req_filtered = req_filtered[req_filtered['center'] == selected_center]
    elif selected_city != "All":
        prob_filtered = prob_filtered.merge(center_info[['center', 'city']], on='center', how='left')
        prob_filtered = prob_filtered[prob_filtered['city'] == selected_city]
        req_filtered = req_filtered.merge(center_info[['center', 'city']], on='center', how='left')
        req_filtered = req_filtered[req_filtered['city'] == selected_city]

    st.markdown("**Recent Problems**")
    if prob_filtered.empty:
        st.info("No problems logged.")
    else:
        st.dataframe(prob_filtered.sort_values('date', ascending=False).head(10), use_container_width=True)

    st.markdown("**Requirements List**")
    if req_filtered.empty:
        st.info("No requirements logged.")
    else:
        st.dataframe(req_filtered, use_container_width=True)

    st.markdown("---")

    # Small map of centers
    st.subheader("Centre Locations")
    map_centers = center_info.copy()
    if selected_center != "All":
        map_centers = map_centers[map_centers['center'] == selected_center]
    elif selected_city != "All":
        map_centers = map_centers[map_centers['city'] == selected_city]

    if not map_centers.empty:
        st.map(map_centers.rename(columns={'lat': 'latitude', 'lon': 'longitude'})[['latitude', 'longitude']])
    else:
        st.info("No centres to show on map for the current filters.")

    st.markdown("---")
    st.info("Tip: Use the filters on the sidebar to narrow down to a city or a single centre. The data here is mock/sample data — connect to your real datasets by replacing the generators with your data loading logic.")
